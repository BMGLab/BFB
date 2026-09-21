"""
bib_colab.py — the student-side helper for BIB Colab assignments.

Why this exists
---------------
Three problems, one small module:

1. Every student must get DIFFERENT data.  If all 80 students analyse the same
   counts matrix, the correct answer is a single number that travels by
   WhatsApp in about four minutes.  Here the dataset is seeded from the
   student number, so a copied answer is not merely dishonest, it is wrong.

2. Students submit incomplete notebooks.  Chasing them costs the instructor
   more time than grading does.  `A.check()` tells the student what is missing
   BEFORE they submit, in class, while it is still cheap to fix.

3. AI use has to be disclosed to be discussable.  The disclosure block is a
   required, validated part of the notebook, not an honour-system footnote.

Student-facing usage (this is the whole API):

    !pip -q install requests && curl -sO https://raw.githubusercontent.com/BMGLab/BFB/main/bib_colab.py
    import bib_colab as bib

    A = bib.start("A03")
    A.whoami(name="Ada Tiryaki", student_no="05220000895", section="EN")

    rng, params = A.dataset()          # seeded from student_no — yours alone

    A.record(1, n_replicates=4, depth_millions=25)
    ...
    A.check()                          # what is still missing?
    A.finish()                         # validate, hash, print receipt code
    A.submit()                         # upload straight to the instructor

Prose answers live in markdown cells that start with `### ANSWER n`.  This
module reads the live notebook to validate them, so the student sees the same
checks the instructor's collector will apply.

Requires nothing outside the standard library plus numpy, which Colab has.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    import numpy as np
except ImportError:  # pragma: no cover - Colab always has numpy
    np = None


# --------------------------------------------------------------------------
# One-click submission endpoint.
#
# When SUBMIT_URL is set, A.submit() uploads the notebook straight into the
# instructor's Drive and the student never downloads a file.  Deploy the Apps
# Script in tools/appsscript/ and paste its /exec URL here.
#
# SUBMIT_TOKEN is NOT a secret from students — this file is public and they can
# read it.  It stops drive-by scanners that find the /exec URL, nothing more.
# Real submission integrity comes from the receipt code and the per-seed data,
# exactly as before.  Leave SUBMIT_URL empty to fall back to the Google Form.
# --------------------------------------------------------------------------

SUBMIT_URL = ("https://script.google.com/macros/s/"
              "AKfycbwf9zbTFxkRSIQLUxCJ88zQev6KA8rhpstEdpsL-D4soEAKRL6XxN0PQKxQ_rt0_hcM/exec")
SUBMIT_TOKEN = "bib-2026"
SUBMIT_MAX_MB = 8.0  # encoded size; Apps Script starts refusing well above this
# Where a student goes when the upload fails. Set FORM_URL to a Google Form if
# you make one; otherwise the fallback names the LMS, which is where these
# notebooks sent work before one-click submission existed.
FORM_URL = ""
FALLBACK_PLACE = "the Week's assignment on EgeDers"


# --------------------------------------------------------------------------
# Assignment definitions.
#
# Add an entry here for each assignment.  `questions` lists the answer numbers
# the student must fill in; `structured` lists the keys `A.record()` expects.
# Keeping this table in one place means the collector and the student helper
# can never disagree about what a complete submission looks like.
# --------------------------------------------------------------------------

ASSIGNMENTS = {
    "A03": {
        "title": "Design an RNA-seq experiment",
        "questions": [1, 2, 3, 4, 5],
        "structured": {
            1: ["n_replicates", "depth_millions"],
            3: ["detected_genes", "false_positives"],
        },
        # Only these keys are treated as integrity evidence by the collector.
        #
        # This distinction matters. A recorded value is only evidence of independent
        # work if it is DERIVED from the student's own seed. `n_replicates` is a
        # design CHOICE — half the class will legitimately pick 6, and flagging that
        # as collusion would bury the real signal. `detected_genes` is computed from
        # a dataset nobody else has, so two students cannot honestly match.
        #
        # Rule when adding an assignment: continuous, seed-derived, computed -> here.
        # Anything the student chose or predicted -> leave it out.
        "integrity_keys": ["detected_genes", "false_positives"],
        "points": 100,
    },
    # ---------------------------------------------------------------------
    # W01-W14: the published BMGLab/BFB weekly notebooks.
    #
    # These predate this module and keep their answers in a RESPONSES dict, so
    # they are declared with answers_from="responses" and A.answers() feeds them
    # in. `structured` is empty because they call no A.record(); A.answers()
    # captures the numeric leaves of RESULTS under Q0 instead.
    #
    # integrity_keys is deliberately EMPTY. The duplicate check is only honest
    # over quantities that provably vary per student, and which RESULTS keys are
    # seed-dependent has not been verified week by week. Claiming them here would
    # generate confident false positives. The per-student SEED is already carried
    # separately, and identical seeds mean a shared COURSE_ID.
    # ---------------------------------------------------------------------
    "W01": {
        "title": "From a biological question to defensible evidence",
        "questions": [1, 2, 3, 4],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W02": {
        "title": "Files, coordinates and reference versions",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W03": {
        "title": "Reading and checking short Python programs",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W04": {
        "title": "Sequence similarity without overclaiming",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W05": {
        "title": "From sample to reads: designing an experiment",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W06": {
        "title": "Variation, independence and multiple testing",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W07": {
        "title": "RNA counts, normalization and defensible expression claims",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W08": {
        "title": "Midterm review and the evidence audit",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W09": {
        "title": "Patterns, prediction and data leakage",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W10": {
        "title": "Single cells and biological replication",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W11": {
        "title": "Biological AI and the honest model scorecard",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W12": {
        "title": "Protein structures: prediction, confidence and function",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W13": {
        "title": "From a variant to an evidence-based sentence",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "W14": {
        "title": "Responsible bioinformatics and your scientific record",
        "questions": [1, 2, 3],
        "structured": {},
        "answers_from": "responses",
        "integrity_keys": [],
        "points": 100,
    },
    "L01": {
        "title": "Zero-install day one: your seed, your notebook, your receipt",
        "questions": [1, 2, 3],
        "structured": {
            1: ["gencode50_transcripts", "gene_span_bp"],
            2: ["model_transcripts", "gencode50_transcripts"],
            3: ["dois_offered", "dois_resolved"],
        },
        # model_transcripts is a transcription of what a model said, and the DOI counts
        # count a third party's output — neither is seed-derived, so neither is evidence.
        "integrity_keys": [
            "gencode50_transcripts", "gene_span_bp"
        ],
        "points": 100,
    },
    "L02": {
        "title": "Coordinate carnage: the off-by-one you will meet every year",
        "questions": [1, 2],
        "structured": {
            1: ["bed_length", "gtf_length"],
            2: ["build_detected", "n_rows_after_intersect"],
        },
        # build_detected is a detection CHOICE with few possible values; out.
        "integrity_keys": [
            "bed_length", "gtf_length", "n_rows_after_intersect"
        ],
        "points": 100,
    },
    "L04": {
        "title": "Hand, then machine, then audit: one alignment two ways",
        "questions": [1, 2, 3],
        "structured": {
            1: ["hand_score", "hand_aligned_len"],
            2: ["lcs_length", "lcs_length_program", "defect_line"],
        },
        # defect_line takes a handful of values across the cohort; never an integrity key.
        "integrity_keys": [
            "hand_score", "hand_aligned_len", "lcs_length", "lcs_length_program"
        ],
        "points": 100,
    },
    "D1": {
        "title": "Design Notebook 1 — design a sequencing experiment and defend the depth",
        "questions": [1, 2, 3, 4, 5],
        "structured": {
            1: ["platform", "coverage_x", "read_length"],
            2: ["callable_frac_10x", "callable_frac_20x"],
            3: ["control_callable_frac"],
            5: ["audit_coverage_reported", "audit_coverage_corrected", "defect_line"],
        },
        # Q1 is the DESIGN the student chose — platform and depth are meant to vary by
        # judgement, not by seed, so they stay out.
        "integrity_keys": [
            "callable_frac_10x", "callable_frac_20x", "control_callable_frac",
            "audit_coverage_reported", "audit_coverage_corrected"
        ],
        # TODO two-stage finish. The spec wants an in-room receipt at minute 30
        #   covering only the seed-derived numbers, then a final receipt after the
        #   at-home DEFEND and AUDIT:
        #   'stages': {'in_room': {'questions': [1, 3], 'structured': [1, 2, 3]},
        #              'final':   {'questions': [1, 3, 4, 5], 'structured': [1, 2, 3, 5]}}
        #   finish()/check()/submit() have no stage parameter yet, so the numbers
        #   below are the FINAL requirements. Running A.submit() at minute 30 will
        #   correctly report the at-home questions as missing.
        "points": 100,
    },
    "A05": {
        "title": "The negative control: how many genes are significant when nothing is happening?",
        "questions": [1, 2, 3],
        "structured": {
            1: ["n_raw_sig", "n_bh_sig"],
            2: ["n_pseudorep_sig", "n_confounded_sig"],
            3: ["n_defective_sig", "n_corrected_sig", "defect_line"],
        },
        # n_corrected_sig is what the fix SHOULD produce, so correct students converge.
        "integrity_keys": [
            "n_raw_sig", "n_bh_sig", "n_pseudorep_sig", "n_confounded_sig",
            "n_defective_sig"
        ],
        "points": 100,
    },
    "A06": {
        "title": "The TPM that isn't: find the order-of-operations bug",
        "questions": [1, 2, 3],
        "structured": {
            1: ["cpm_gene_a", "cpm_gene_b"],
            2: ["colsum_before_fix", "tpm_gene_a", "tpm_gene_b", "defect_line"],
            3: ["ensg_septin2", "ensg_marchf1", "ensg_delec1"],
        },
        # The ENSG lookups in Q3 are facts about the annotation — identical for everyone
        # by design, which is the whole point of that question.
        "integrity_keys": [
            "cpm_gene_a", "cpm_gene_b", "colsum_before_fix", "tpm_gene_a", "tpm_gene_b"
        ],
        "points": 100,
    },
    "A07": {
        "title": "The AI Output Audit: mark every claim SUPPORTED / WRONG / UNVERIFIABLE",
        "questions": [1, 2, 3],
        "structured": {
            1: ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"],
            2: ["src_a", "src_b"],
            3: ["tpm_colsum_s1", "n_sig_wrong_denominator", "n_sig_correct_denominator"],
        },
        # v1-v8 are verdicts from a three-value menu and src_a/src_b are citations —
        # agreement there is the marking scheme working, not collusion.
        # n_sig_correct_denominator is the right answer, so it converges too.
        "integrity_keys": [
            "tpm_colsum_s1", "n_sig_wrong_denominator"
        ],
        "points": 100,
    },
    "D2": {
        "title": "Design Notebook 2 — split it wrong, split it right, then shuffle the labels",
        "questions": [1, 2, 3, 4, 5, 6],
        "structured": {
            1: ["baseline_acc"],
            2: ["leaky_acc", "pipeline_acc"],
            3: ["grouped_acc", "shuffled_acc"],
            5: ["audit_reported_acc", "audit_corrected_acc", "defect_line"],
            6: ["acc_cohort_a", "acc_cohort_b"],
        },
        # Every accuracy here is computed from the student's own split seed.
        "integrity_keys": [
            "baseline_acc", "leaky_acc", "pipeline_acc", "grouped_acc", "shuffled_acc",
            "audit_reported_acc", "audit_corrected_acc", "acc_cohort_a", "acc_cohort_b"
        ],
        # TODO two-stage finish. The spec wants an in-room receipt at minute 30
        #   covering only the seed-derived numbers, then a final receipt after the
        #   at-home DEFEND and AUDIT:
        #   'in_room' covers Q1-Q3; 'final' adds Q4-Q6.
        #   finish()/check()/submit() have no stage parameter yet, so the numbers
        #   below are the FINAL requirements. Running A.submit() at minute 30 will
        #   correctly report the at-home questions as missing.
        "points": 100,
    },
    "L03": {
        # Week 3 application hour — see 02-labs/week-03-lab-l03-spec.md.
        "title": "Trace it, predict it, break it",
        "questions": [1, 2, 3],
        "structured": {
            2: ["hand_value", "func_value", "defect_line"],
        },
        # hand_value and func_value are computed from the dealt sequence;
        # defect_line takes only four values, so it is expected-checked but
        # deliberately NOT integrity evidence (see the spec, Q2 note).
        "integrity_keys": ["hand_value", "func_value"],
        "points": 100,
    },
}

# --------------------------------------------------------------------------
# What A.dataset() deals, per assignment.  Each dealer takes the student's
# seeded generator and returns the `params` dict that dataset() prints.  Keys
# that start with "_" are returned but not printed (the notebook reads them;
# the header does not announce them).
# --------------------------------------------------------------------------

def _deal_a03(rng):
    return {
        "n_genes": 12000,
        # These ranges are calibrated, not arbitrary. They keep every student
        # inside a band where a 3-replicate design detects almost nothing, a
        # 6-replicate design at the same total read budget detects most of the
        # signal, and going beyond ~8 replicates buys very little. That is the
        # lesson of the assignment, so the numbers have to produce it.
        "true_lfc": round(float(rng.uniform(0.8, 1.4)), 3),
        "dispersion": round(float(rng.uniform(0.02, 0.05)), 4),
        "n_truly_de": int(rng.integers(150, 600)),
        "lib_size_cv": round(float(rng.uniform(0.10, 0.35)), 3),
        "budget_million_reads": int(rng.choice([150, 200, 250, 300])),
    }


def _l03_hand_bank(n=40, build_seed=20260913):
    """
    The five-base hand-check strings for L03 (spec: 'seeded_per_student').
    Every string is chosen so that each of the four planted variants of
    score_bases() returns something OTHER than the true purine count:
      V1 skips seq[0]  -> seq[0] must be a purine
      V2 skips seq[4]  -> seq[4] must be a purine
      V3 tests seq[1] on every pass -> returns 0 or 5, so truth in {2, 3}
      V4 counts pyrimidines -> returns 5 - truth, so truth != 2.5 (always)
    """
    if np is None:  # pragma: no cover
        return []
    from itertools import product
    keep = []
    for t in product("ACGT", repeat=5):
        s = "".join(t)
        truth = sum(b in "AG" for b in s)
        if s[0] not in "AG" or s[4] not in "AG" or truth not in (2, 3):
            continue
        v3 = 5 if s[1] in "AG" else 0
        assert truth - 1 != truth and v3 != truth and 5 - truth != truth
        keep.append(s)
    r = np.random.default_rng(build_seed)
    return sorted(r.choice(keep, size=n, replace=False).tolist())


_L03_HAND_BANK = _l03_hand_bank()


def _deal_l03(rng):
    # NOTE: the spec derives seq_id and the defect variant from the roster
    # rank. ROSTER_ORDER is not in this module yet, so both are drawn from the
    # student's seeded rng for now — still unique per student, still checkable.
    return {
        "seq_id": f"seq{1 + int(rng.integers(20)):02d}",
        "hand_seq": _L03_HAND_BANK[int(rng.integers(len(_L03_HAND_BANK)))],
        "count_table": rng.integers(0, 501, size=(3, 4)),
        "_defect_variant": 1 + int(rng.integers(4)),
    }


DEALS = {"A03": _deal_a03, "L03": _deal_l03}


# SHA-256 of each enrolled student number, e.g. {"3a7f...", ...}.
#
# Leave empty and any well-formed number is accepted. Populate it (see
# `make_roster_hashes()` at the bottom of this file) and a mistyped digit is
# rejected in the room, where a TA fixes it in ten seconds — rather than silently
# generating a valid-looking dataset that belongs to nobody, which the collector
# only catches days later.
ROSTER_HASHES = set()

# A name part: a letter, then letters/apostrophes/hyphens. Covers Turkish
# diacritics and hyphenated surnames; rejects "test", "asdf" and "x".
NAME_PART_RE = re.compile(r"[^\W\d_][\w'\u2019.-]+", re.UNICODE)

DISCLOSURE_HEADING = "### AI DISCLOSURE"
ANSWER_RE = re.compile(r"^#{2,4}\s*ANSWER\s+(\d+)\b", re.IGNORECASE | re.MULTILINE)

# The W-series notebooks keep answers in a RESPONSES dict, not in markdown cells.
# A.answers() echoes them into the cell OUTPUT in these canonical blocks so that one
# representation serves the student, the receipt hash and the collector alike.
ANSWER_OUT_RE = re.compile(r"^### ANSWER (\d+)\n(.*?)\n### END ANSWER \1$", re.M | re.S)
DISCLOSURE_OUT_RE = re.compile(
    r"^### AI DISCLOSURE\n(.*?)\n### END AI DISCLOSURE$", re.M | re.S)

# Text that still sits in the template means the student did not write anything.
PLACEHOLDER_MARKERS = (
    "your answer here",
    "buraya yazınız",
    "buraya yaziniz",
    "write your answer",
    "...",
    "todo",
)


def in_colab():
    """True when running inside Google Colab."""
    try:
        import google.colab  # type: ignore  # noqa: F401

        return True
    except ImportError:
        return False


def _get_live_notebook():
    """
    Return the current notebook as a dict, or None if it cannot be read.

    Colab exposes the notebook JSON over an internal, undocumented message
    channel. It could stop working after any Colab release, so every failure
    falls through to None — but see finish(): inside Colab, None is FATAL, not a
    warning. If we cannot see the notebook we cannot verify the prose answers,
    and issuing a receipt anyway would certify submissions nobody checked.
    """
    try:
        from google.colab import _message  # type: ignore

        return _message.blocking_request("get_ipynb", request="", timeout_sec=30)["ipynb"]
    except Exception:
        return None


def _post_json(url, obj, timeout=90, attempts=3):
    """
    POST `obj` as JSON and return (ok, reply_dict).

    Retries, because this runs in a teaching lab on shared wifi and a single
    dropped packet should not cost a student their submission.  Apps Script
    answers a POST with a 302 to googleusercontent; urllib follows it, which is
    why this needs no third-party library.
    """
    data = json.dumps(obj).encode("utf-8")
    detail = "no attempt made"
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
            try:
                return True, json.loads(raw)
            except json.JSONDecodeError:
                # Almost always a Google sign-in page: the web app was deployed
                # with the wrong access setting.
                detail = "the server replied with a web page, not a result"
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                # Google rejected the request before the script ran. Retrying
                # cannot help, and it is always the same misconfiguration.
                return False, {"error": (
                    f"HTTP {exc.code} — Google refused the request before the "
                    "submission script ran. The web app is not published to "
                    "'Anyone'. Instructor: Deploy > Manage deployments > edit > "
                    "Who has access: Anyone > New version > Deploy.")}
            detail = f"HTTP {exc.code}: {exc.reason}"
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
        if attempt < attempts - 1:
            time.sleep(2 * (attempt + 1))
    return False, {"error": detail}


def canonical_payload(assignment, student_no, answers, disclosure, structured):
    """
    Canonical text form of a submission.

    Both sides compute this: the student's session from the live notebook, and
    the instructor's collector from the downloaded .ipynb. The receipt code is a
    hash of it, so if a student edits an answer after running finish() the
    recomputed hash no longer matches the printed receipt and the collector says
    so. That is what makes the receipt mean something rather than being a
    decorative string.

    `structured` values must already be the printed "k=v, k=v" form so the two
    sides cannot drift apart.
    """
    def norm(text):
        # Drop the heading line; collapse all whitespace.
        body = "\n".join(str(text).strip().splitlines()[1:])
        return " ".join(body.split())

    parts = [f"assignment={assignment}", f"student={student_no}"]
    for q in sorted(answers):
        parts.append(f"A{q}={norm(answers[q])}")
    parts.append(f"D={norm(disclosure or '')}")
    for q in sorted(structured):
        parts.append(f"R{q}={structured[q]}")
    return "\n".join(parts)


def receipt_for(payload):
    """The 10-character receipt code for a canonical payload."""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:10].upper()


def make_roster_hashes(student_numbers):
    """
    Helper for the instructor: turn a list of student numbers into the set to
    paste into ROSTER_HASHES. Raw numbers are never stored in the file.

        python3 -c "import bib_colab,csv; \
          print(bib_colab.make_roster_hashes(r['student_no'] for r in csv.DictReader(open('roster.csv'))))"
    """
    return {hashlib.sha256(str(n).strip().encode()).hexdigest() for n in student_numbers}


def _flatten_numbers(obj, prefix=""):
    """
    Numeric leaves of a nested dict, as flat `a.b` keys.

    The W notebooks build a nested RESULTS dict whose shape differs every week,
    so the values worth carrying into the submission cannot be named in advance.
    Booleans are excluded: bool is a subclass of int, and True/False carries no
    evidence of independent work.
    """
    out = {}
    for k, v in (obj or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten_numbers(v, f"{key}."))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out[key] = v
    return out


def _cell_text(cell):
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def _is_placeholder(text):
    stripped = text.strip().lower()
    if not stripped:
        return True
    # Strip the heading line, then see whether anything of substance remains.
    body = "\n".join(stripped.splitlines()[1:]).strip()
    if not body:
        return True
    return any(body == m or body.startswith(m) for m in PLACEHOLDER_MARKERS)


class Assignment:
    def __init__(self, code):
        if code not in ASSIGNMENTS:
            raise ValueError(
                f"Unknown assignment {code!r}. Known: {', '.join(sorted(ASSIGNMENTS))}"
            )
        self.code = code
        self.spec = ASSIGNMENTS[code]
        self.student = {}
        self.structured = {}
        self._seed = None
        self._prose = None        # set by answers(), dict-mode only
        self._disclosure = None

    # -- identity ----------------------------------------------------------

    def whoami(self, name, student_no, section):
        """Record identity and derive this student's private random seed."""
        student_no = str(student_no).strip()
        if not re.fullmatch(r"\d{6,15}", student_no):
            raise ValueError(
                f"student_no should be your Ege student number, digits only — got {student_no!r}"
            )
        section = section.strip().upper()
        if section not in ("EN", "TR"):
            raise ValueError("section must be 'EN' or 'TR'")
        # Same rule the endpoint enforces. Checking it here too means a student
        # who types 'ada' is told so in the room, not by a server after the lab.
        name = " ".join(str(name).split())
        parts = name.split(" ")
        if len(parts) < 2 or not all(NAME_PART_RE.fullmatch(w) for w in parts):
            raise ValueError(
                "give your full name as it appears on the roster — at least two "
                f"words, letters only (got {name!r})")
        if ROSTER_HASHES:
            digest = hashlib.sha256(student_no.encode()).hexdigest()
            if digest not in ROSTER_HASHES:
                raise ValueError(
                    f"{student_no} is not on the class roster for this course.\n"
                    "Check every digit. If it is definitely correct, tell the "
                    "instructor now — do not continue, because a wrong number "
                    "gives you a dataset that belongs to nobody."
                )

        self.student = {"name": name, "student_no": student_no, "section": section}
        self._seed = int(hashlib.sha256(student_no.encode()).hexdigest()[:8], 16)

        print(f"{self.code} — {self.spec['title']}")
        print(f"{self.student['name']}  |  {student_no}  |  section {section}")
        print(f"your dataset seed: {self._seed}")
        print("\nThis seed is derived from your student number. Your data is not the")
        print("same as anyone else's, so a borrowed answer will be the wrong answer.")
        return self.student

    # -- data --------------------------------------------------------------

    def dataset(self):
        """
        Return `(rng, params)` for this student.

        `params` carries the per-student experimental scenario: effect size,
        dispersion and library-size variability.  Two students therefore face
        genuinely different design problems, not the same problem with
        different noise.
        """
        self._require_identity()
        if np is None:
            raise RuntimeError("numpy is required; run this in Colab or `pip install numpy`")

        rng = np.random.default_rng(self._seed)
        # Every lab is declared in ASSIGNMENTS so that submission works, but the
        # per-lab dealers are built week by week. Falling back to another lab's
        # dealer here would hand a student plausible numbers from the WRONG
        # experiment and nothing downstream would notice. Refuse instead.
        if self.code not in DEALS:
            raise NotImplementedError(
                f"{self.code} accepts submissions, but its dataset dealer is not built "
                f"yet. Built: {', '.join(sorted(DEALS))}.")
        params = DEALS[self.code](rng)
        print("Your scenario:")
        for k, v in params.items():
            if k.startswith("_"):
                continue                      # dealt, but not announced
            shown = f"array, shape {v.shape}" if hasattr(v, "shape") else v
            print(f"  {k:24s} {shown}")
        return rng, params

    # -- answers -----------------------------------------------------------

    def record(self, question, **values):
        """Record the structured (numeric) part of an answer."""
        self._require_identity()
        expected = self.spec["structured"].get(question)
        if expected is None:
            raise ValueError(
                f"Question {question} takes no structured values — write prose under "
                f"'### ANSWER {question}' instead."
            )
        missing = [k for k in expected if k not in values]
        if missing:
            raise ValueError(f"Question {question} also needs: {', '.join(missing)}")
        unexpected = [k for k in values if k not in expected]
        if unexpected:
            raise ValueError(
                f"Question {question} does not take {', '.join(unexpected)}. "
                f"Expected: {', '.join(expected)}"
            )
        self.structured[question] = {k: values[k] for k in expected}
        shown = ", ".join(f"{k}={v}" for k, v in self.structured[question].items())
        print(f"recorded Q{question}: {shown}")

    # -- validation --------------------------------------------------------

    def _scan_notebook(self):
        """Find prose answers and the disclosure block in the live notebook."""
        if self.spec.get("answers_from") == "responses":
            # Answers came from A.answers(), so there is nothing to scan and
            # nothing that can go stale between the dict and the notebook.
            if self._prose is None:
                return {"answers": {}, "disclosure": None}
            return {"answers": self._prose, "disclosure": self._disclosure}
        nb = _get_live_notebook()
        if nb is None:
            return None
        found, disclosure = {}, None
        for cell in nb.get("cells", []):
            if cell.get("cell_type") != "markdown":
                continue
            text = _cell_text(cell)
            m = ANSWER_RE.search(text)
            if m:
                n = int(m.group(1))
                # Keep the longest cell if a student duplicates a heading.
                if n not in found or len(text) > len(found[n]):
                    found[n] = text
            if DISCLOSURE_HEADING.lower() in text.lower():
                disclosure = text
        return {"answers": found, "disclosure": disclosure}

    def answers(self, responses, prediction="", check="", disclosure="", results=None):
        """
        Submit answers held in a dict, for notebooks that collect them that way.

        The W-series notebooks were written before this module existed and keep
        their answers in `RESPONSES = {"Q1": ...}`. Rather than rewrite fourteen
        notebooks into the markdown-cell convention, this takes the dict and
        echoes it into the cell output in the same canonical form the collector
        already parses. Nothing about how a student fills those notebooks changes.

        `prediction` and `check` are hashed alongside the disclosure, so editing
        them after submitting breaks the receipt exactly as editing an answer does.
        """
        if self.spec.get("answers_from") != "responses":
            raise RuntimeError(
                f"{self.code} expects prose in '### ANSWER n' markdown cells, "
                "not A.answers(). Write your answers in the cells and run A.check().")

        self._prose = {}
        for key, text in sorted(responses.items()):
            m = re.fullmatch(r"[Qq](\d+)", str(key).strip())
            if not m:
                raise ValueError(f"RESPONSES keys must look like 'Q1', got {key!r}")
            n = int(m.group(1))
            body = str(text).strip()
            self._prose[n] = f"### ANSWER {n}\n{body}"
            print(f"### ANSWER {n}\n{body}\n### END ANSWER {n}")

        blob = (f"{str(disclosure).strip()}\n\n"
                f"PREDICTION: {str(prediction).strip()}\n\n"
                f"CHECK PERFORMED: {str(check).strip()}")
        self._disclosure = f"{DISCLOSURE_HEADING}\n{blob}"
        print(f"{DISCLOSURE_HEADING}\n{blob}\n### END AI DISCLOSURE")

        if results:
            flat = _flatten_numbers(results)
            if flat:
                self.structured[0] = flat
                print("recorded Q0: " + ", ".join(f"{k}={v}" for k, v in flat.items()))
        return self

    def check(self, quiet=False):
        """Report what is still missing. Returns a list of problems."""
        problems = []
        if not self.student:
            problems.append("identity not set — call A.whoami(...) in the cell at the top")

        for q, keys in self.spec["structured"].items():
            if q not in self.structured:
                problems.append(f"Q{q}: no A.record({q}, {', '.join(k + '=...' for k in keys)}) yet")

        scan = self._scan_notebook()
        if scan is None:
            problems.append(
                "cannot read this notebook to check prose answers "
                "(that is normal outside Colab — check them yourself)"
            )
        else:
            for q in self.spec["questions"]:
                text = scan["answers"].get(q)
                if text is None:
                    problems.append(
                        f"Q{q}: not submitted — run the A.answers(RESPONSES, ...) cell"
                        if self.spec.get("answers_from") == "responses"
                        else f"Q{q}: no '### ANSWER {q}' markdown cell found")
                elif _is_placeholder(text):
                    problems.append(f"Q{q}: the ANSWER cell is still empty or still says 'your answer here'")
            if scan["disclosure"] is None:
                problems.append(f"no '{DISCLOSURE_HEADING}' cell found — it is required")
            elif _is_placeholder(scan["disclosure"]):
                problems.append(f"'{DISCLOSURE_HEADING}' is empty — say what you used AI for, honestly")

        if not quiet:
            if problems:
                print(f"{len(problems)} thing(s) to fix before you submit:\n")
                for p in problems:
                    print(textwrap.fill(f"  - {p}", 88, subsequent_indent="    "))
            else:
                if SUBMIT_URL:
                    print("Everything required is present. Run A.submit() to send it in.")
                else:
                    print("Everything required is present. Run A.finish() to get your receipt code.")
        return problems

    def finish(self, _announce=True):
        """
        Validate, then print the receipt code.

        `_announce=False` is used by submit(): the receipt banner still prints,
        but the "now upload it yourself" instructions are suppressed because
        submit() is about to do the uploading.
        """
        scan = self._scan_notebook()

        # Fail CLOSED. If we are in Colab but cannot read the notebook, we cannot
        # confirm a single prose answer exists. Issuing a receipt here would
        # certify work nobody verified, and the instructor would discover it days
        # later at the collector. Refuse instead, loudly, with a way forward.
        if scan is None and in_colab() and self.spec.get("answers_from") != "responses":
            print("CANNOT VERIFY THIS NOTEBOOK — no receipt issued.\n")
            print(textwrap.fill(
                "  The check that reads your notebook did not respond. This is a "
                "Colab problem, not something you did wrong.", 88,
                subsequent_indent="  "))
            print("\n  Try, in order:")
            print("    1. Runtime > Restart session and run all, then run this cell again.")
            print("    2. Reload the browser tab and re-run.")
            print("    3. If it still fails, submit the notebook anyway and write")
            print("       NO-RECEIPT in the receipt field of the form. You will not")
            print("       be penalised — but tell your instructor today.")
            return None

        problems = self.check(quiet=True)
        blocking = [p for p in problems if not p.startswith("cannot read this notebook")]
        if blocking:
            print("NOT READY — fix these first:\n")
            for p in blocking:
                print(textwrap.fill(f"  - {p}", 88, subsequent_indent="    "))
            print("\nThen run A.%s() again." % ("finish" if _announce else "submit"))
            return None

        if scan is None:
            # Outside Colab: the instructor testing locally. Allowed, but say so.
            print("WARNING: not running in Colab, so prose answers were not verified.")
            print("         This receipt is for testing only.\n")
            scan = {"answers": {}, "disclosure": None}

        printed = {q: ", ".join(f"{k}={v}" for k, v in vals.items())
                   for q, vals in self.structured.items()}
        payload = canonical_payload(self.code, self.student["student_no"],
                                    scan["answers"], scan["disclosure"], printed)
        receipt = receipt_for(payload)

        with open("bib_submission.json", "w", encoding="utf-8") as fh:
            json.dump({"assignment": self.code, "student": self.student,
                       "seed": self._seed, "structured": self.structured,
                       "receipt": receipt,
                       "submitted_utc": datetime.now(timezone.utc)
                                        .strftime("%Y-%m-%dT%H:%M:%SZ")},
                      fh, indent=2, ensure_ascii=False)

        print("=" * 62)
        print(f"  RECEIPT CODE:  {receipt}")
        print("=" * 62)
        print(f"  {self.student['name']} | {self.student['student_no']} | {self.student['section']}")
        print(f"  {self.code} — {self.spec['title']}")
        if not _announce:
            return receipt

        if SUBMIT_URL:
            print("\n  One thing left:  run  A.submit()  in the last cell.")
            print("  It sends this notebook straight to your instructor —")
            print("  no downloading, no form, no attachment.")
        else:
            print("\n  Now do BOTH of these:")
            print("    1. File > Download > Download .ipynb")
            print("    2. Upload that file to the submission form and paste the")
            print("       receipt code above into the form.")
        print("\n  This code is computed from the text of your answers. If you edit")
        print("  anything after this point, re-run this cell to get a new one —")
        print("  otherwise the code will not match what you submit.")
        return receipt

    def submit(self):
        """
        Validate and upload this notebook to the instructor's Drive. One call,
        one cell, nothing for the student to download or attach.

        Note the asymmetry with finish(), which fails CLOSED: if finish() cannot
        read the notebook it refuses a receipt, because certifying unverified
        work is worse than refusing.  submit() fails OPEN: if the network or the
        endpoint is down, it says so and prints the manual fallback.  A student
        who did the work must never be blocked by transport.
        """
        if not SUBMIT_URL:
            print("Direct submission is not set up for this course.")
            print("Run A.finish() and upload your notebook to the form instead.")
            return None

        receipt = self.finish(_announce=False)
        if receipt is None:
            return None  # finish() has already said exactly what is wrong

        nb = _get_live_notebook()
        if nb is None:
            # finish() would have refused in Colab, so this is the local case.
            print("\nNot running in Colab — there is no notebook to upload.")
            return None

        raw = json.dumps(nb, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        packed = base64.b64encode(gzip.compress(raw, 6)).decode("ascii")
        size_mb = len(packed) / 1e6
        if size_mb > SUBMIT_MAX_MB:
            print(f"\nThis notebook is too big to send ({size_mb:.1f} MB).")
            print("Usually that means one cell printed thousands of lines, or a")
            print("figure was drawn hundreds of times in a loop. Clear that cell's")
            print("output (click the ⋮ beside it > Clear output) and run A.submit()")
            print(f"again. If you cannot find it, upload the .ipynb to {FORM_URL or FALLBACK_PLACE}.")
            return None

        shown = f"{size_mb:.1f} MB" if size_mb >= 1 else f"{len(packed) / 1e3:.0f} KB"
        print(f"\nSending {shown} …")
        ok, reply = _post_json(SUBMIT_URL, {
            "token": SUBMIT_TOKEN,
            "assignment": self.code,
            "student_no": self.student["student_no"],
            "name": self.student["name"],
            "section": self.student["section"],
            "receipt": receipt,
            "seed": self._seed,
            "structured": {str(q): v for q, v in self.structured.items()},
            "client_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "notebook_gz_b64": packed,
        })

        # A reply must carry a ref to count as saved. Apps Script answers a POST
        # with a redirect, and if the GET that follows it lands on doGet instead
        # of the stored doPost result, the body is {"status":"ok", ...} with no
        # ref — a shape that would otherwise print SUBMITTED over a submission
        # that was never written. Seen once in testing; harmless now.
        if ok and reply.get("status") == "ok" and not reply.get("ref"):
            ok, reply = False, {"error": (
                "the server acknowledged without saving anything (no reference "
                "returned). Run A.submit() again — this is usually transient.")}

        if ok and reply.get("status") == "ok":
            print("=" * 62)
            print(f"  SUBMITTED.  Reference: {reply.get('ref', '?')}")
            print("=" * 62)
            print(f"  {self.code} · {self.student['name']} · {self.student['student_no']}")
            print(f"  Receipt {receipt} · {reply.get('saved_utc', '')}")
            print("\n  Your instructor now has this notebook. You can close the tab.")
            print("  Changed your mind? Fix it, run A.submit() again — the newest")
            print("  submission is the one that counts.")
            return reply.get("ref")

        reason = reply.get("error", "unknown") if isinstance(reply, dict) else "unknown"
        print("UPLOAD FAILED — but you have NOT lost your work.\n")
        print(textwrap.fill(f"  Reason: {reason}", 88, subsequent_indent="          "))
        where = FORM_URL if FORM_URL else FALLBACK_PLACE
        print("\n  Do this instead, now, before you leave:")
        print("    1. File > Download > Download .ipynb")
        print(f"    2. Upload that file to {where}")
        print(f"    3. Put this receipt code in the submission comment:  {receipt}")
        print("\n  Then tell your instructor the upload button failed —")
        print("  you will not be penalised, but they need to know today.")
        return None

    # -- internals ---------------------------------------------------------

    def _require_identity(self):
        if not self.student:
            raise RuntimeError("call A.whoami(name=..., student_no=..., section=...) first")


def start(code):
    """Begin an assignment. `code` is e.g. "A03"."""
    a = Assignment(code)
    spec = a.spec
    print(f"BIB {code} — {spec['title']}  ({spec['points']} points)")
    print(f"Questions to answer: {', '.join('Q' + str(q) for q in spec['questions'])}")
    print("\nNext: fill in the A.whoami(...) cell below.")
    return a


if __name__ == "__main__":
    print(__doc__)
    print("Known assignments:")
    for code, spec in sorted(ASSIGNMENTS.items()):
        print(f"  {code}: {spec['title']}")
    sys.exit(0)
