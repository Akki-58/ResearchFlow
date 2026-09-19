import re
import time
from statistics import mean


class ResearchMetrics:
    """
    Metrics collector for a multi-agent research pipeline.

    Tracks:
    - Pipeline latency
    - Number of revisions
    - Critic scores
    - Pass/revise decisions
    - Source counts
    - Report size
    - Quality improvement
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

        self.iterations = []

        self.search_source_count = 0
        self.scraped_source_count = 0

        self.report_word_count = 0

    # --------------------------------------------------
    # Pipeline timing
    # --------------------------------------------------

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    @property
    def latency_seconds(self):
        if self.start_time is None or self.end_time is None:
            return 0

        return round(
            self.end_time - self.start_time,
            2
        )

    # --------------------------------------------------
    # Source metrics
    # --------------------------------------------------

    def count_search_sources(self, search_results: str):
        """
        Counts URLs returned by the search agent.
        """
        urls = re.findall(
            r"https?://[^\s<>]+",
            search_results
        )

        self.search_source_count = len(set(urls))

    def count_scraped_sources(self, scraped_content: str):
        """
        Counts SELECTED URL entries produced by reader agent.
        """
        urls = re.findall(
            r"SELECTED URL:\s*(https?://\S+)",
            scraped_content,
            re.IGNORECASE
        )

        if urls:
            self.scraped_source_count = len(set(urls))
        else:
            # fallback: count URLs
            urls = re.findall(
                r"https?://[^\s<>]+",
                scraped_content
            )

            self.scraped_source_count = len(set(urls))

    # --------------------------------------------------
    # Critic metrics
    # --------------------------------------------------

    @staticmethod
    def extract_score(feedback: str):
        """
        Extracts:

        SCORE: 8/10

        Returns:
            8.0
        """

        match = re.search(
            r"SCORE:\s*(\d+(?:\.\d+)?)\s*/\s*10",
            feedback,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

        return None

    @staticmethod
    def extract_verdict(feedback: str):
        """
        Extracts PASS or REVISE.
        """

        match = re.search(
            r"FINAL VERDICT:\s*(PASS|REVISE)",
            feedback,
            re.IGNORECASE
        )

        if match:
            return match.group(1).upper()

        return "UNKNOWN"

    def add_iteration(
        self,
        iteration_number: int,
        report: str,
        feedback: str
    ):
        score = self.extract_score(feedback)
        verdict = self.extract_verdict(feedback)

        self.iterations.append({
            "iteration": iteration_number,
            "score": score,
            "verdict": verdict,
            "report_words": len(report.split())
        })

    # --------------------------------------------------
    # Report metrics
    # --------------------------------------------------

    def calculate_report_metrics(self, report: str):
        self.report_word_count = len(report.split())

    # --------------------------------------------------
    # Final metrics
    # --------------------------------------------------

    def calculate(self):

        scores = [
            item["score"]
            for item in self.iterations
            if item["score"] is not None
        ]

        pass_count = sum(
            item["verdict"] == "PASS"
            for item in self.iterations
        )

        revise_count = sum(
            item["verdict"] == "REVISE"
            for item in self.iterations
        )

        first_score = scores[0] if scores else None
        final_score = scores[-1] if scores else None

        if first_score is not None and final_score is not None:
            score_improvement = round(
                final_score - first_score,
                2
            )
        else:
            score_improvement = None

        if self.search_source_count:
            source_utilization = round(
                (
                    self.scraped_source_count
                    / self.search_source_count
                ) * 100,
                2
            )
        else:
            source_utilization = 0

        return {
            "latency_seconds": self.latency_seconds,

            "search_sources": self.search_source_count,

            "scraped_sources": self.scraped_source_count,

            "source_utilization_percent":
                source_utilization,

            "total_iterations":
                len(self.iterations),

            "revisions":
                max(len(self.iterations) - 1, 0),

            "first_critic_score":
                first_score,

            "final_critic_score":
                final_score,

            "score_improvement":
                score_improvement,

            "pass_count":
                pass_count,

            "revise_count":
                revise_count,

            "final_verdict":
                (
                    self.iterations[-1]["verdict"]
                    if self.iterations
                    else "UNKNOWN"
                ),

            "report_word_count":
                self.report_word_count,
        }

    # --------------------------------------------------
    # Pretty output
    # --------------------------------------------------

    def print_metrics(self):

        metrics = self.calculate()

        print("\n")
        print("=" * 60)
        print("RESEARCH PIPELINE METRICS")
        print("=" * 60)

        print(
            f"Pipeline latency       : "
            f"{metrics['latency_seconds']} sec"
        )

        print(
            f"Search sources         : "
            f"{metrics['search_sources']}"
        )

        print(
            f"Scraped sources        : "
            f"{metrics['scraped_sources']}"
        )

        print(
            f"Source utilization     : "
            f"{metrics['source_utilization_percent']}%"
        )

        print(
            f"Total iterations       : "
            f"{metrics['total_iterations']}"
        )

        print(
            f"Revisions              : "
            f"{metrics['revisions']}"
        )

        print(
            f"First critic score     : "
            f"{metrics['first_critic_score']}/10"
        )

        print(
            f"Final critic score     : "
            f"{metrics['final_critic_score']}/10"
        )

        print(
            f"Score improvement      : "
            f"+{metrics['score_improvement']}"
        )

        print(
            f"PASS decisions         : "
            f"{metrics['pass_count']}"
        )

        print(
            f"REVISE decisions       : "
            f"{metrics['revise_count']}"
        )

        print(
            f"Final verdict          : "
            f"{metrics['final_verdict']}"
        )

        print(
            f"Report word count      : "
            f"{metrics['report_word_count']}"
        )

        print("=" * 60)
