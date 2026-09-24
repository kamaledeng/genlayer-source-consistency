# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import genlayer.gl as gl


class SourceConsistency(gl.Contract):

    source_a: str
    source_b: str
    verdict: str
    explanation: str

    def __init__(self):
        self.source_a = ""
        self.source_b = ""
        self.verdict = ""
        self.explanation = ""

    @gl.public.write
    def compare_sources(self, source_a: str, source_b: str):

        def leader_fn():
            page_a = gl.nondet.web.get(source_a)
            page_b = gl.nondet.web.get(source_b)

            content_a = page_a.body.decode("utf-8", errors="ignore")[:10000]
            content_b = page_b.body.decode("utf-8", errors="ignore")[:10000]

            prompt = f"""
You are comparing two web sources.

SOURCE A:
{content_a}

SOURCE B:
{content_b}

Determine whether the two sources are broadly consistent about
the factual information they present.

Return JSON with exactly these fields:

{{
  "verdict": "consistent" or "conflicting",
  "explanation": "brief explanation"
}}

Base the decision only on the provided source content.
Do not use outside knowledge.
"""

            return gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

        def validator_fn(leader_result):

            if not isinstance(leader_result, gl.vm.Return):
                return False

            validator_result = leader_fn()

            if not isinstance(validator_result, dict):
                return False

            if not isinstance(leader_result.calldata, dict):
                return False

            leader_verdict = leader_result.calldata.get("verdict")
            validator_verdict = validator_result.get("verdict")

            return (
                leader_verdict in ("consistent", "conflicting")
                and validator_verdict in ("consistent", "conflicting")
                and leader_verdict == validator_verdict
            )

        result = gl.vm.run_nondet_unsafe(
            leader_fn,
            validator_fn
        )

        self.source_a = source_a
        self.source_b = source_b
        self.verdict = result["verdict"]
        self.explanation = result["explanation"]

        return {
            "source_a": self.source_a,
            "source_b": self.source_b,
            "verdict": self.verdict,
            "explanation": self.explanation
        }

    @gl.public.view
    def get_result(self):
        return {
            "source_a": self.source_a,
            "source_b": self.source_b,
            "verdict": self.verdict,
            "explanation": self.explanation
        }
