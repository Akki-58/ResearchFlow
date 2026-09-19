import csv
import json
import time
from datetime import datetime

from pipeline import run_research_pipeline


# ============================================================
# Topics to benchmark
# ============================================================

TOPICS = [
    "Impact of artificial intelligence on software engineering",
    "Large language models in healthcare",
    "Future of autonomous vehicles",
    "Cybersecurity risks of generative AI",
    "AI agents and the future of automation",
    "Renewable energy storage technologies",
    "Quantum computing applications",
    "AI regulation and governance",
    "Edge computing and artificial intelligence",
    "Future of robotics",
]


# ============================================================
# Configuration
# ============================================================

OUTPUT_JSON = "benchmark_results.json"
OUTPUT_CSV = "benchmark_results.csv"
SUMMARY_JSON = "benchmark_summary.json"


# ============================================================
# Run benchmark
# ============================================================

def run_benchmark(topics):

    results = []

    total_start = time.perf_counter()

    print("\n")
    print("=" * 70)
    print("MULTI-AGENT RESEARCH SYSTEM BENCHMARK")
    print("=" * 70)

    print(f"\nNumber of topics: {len(topics)}")

    for index, topic in enumerate(topics, start=1):

        print("\n")
        print("=" * 70)
        print(f"TOPIC {index}/{len(topics)}")
        print("=" * 70)

        print(f"\nTopic: {topic}")

        run_start = time.perf_counter()

        try:

            state = run_research_pipeline(topic)

            run_time = time.perf_counter() - run_start

            metrics = state.get("metrics", {})

            result = {
                "run_id": index,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),

                "status": "SUCCESS",

                "latency_seconds":
                    metrics.get("latency_seconds"),

                "search_sources":
                    metrics.get("search_sources"),

                "scraped_sources":
                    metrics.get("scraped_sources"),

                "source_utilization_percent":
                    metrics.get("source_utilization_percent"),

                "total_iterations":
                    metrics.get("total_iterations"),

                "revisions":
                    metrics.get("revisions"),

                "first_critic_score":
                    metrics.get("first_critic_score"),

                "final_critic_score":
                    metrics.get("final_critic_score"),

                "score_improvement":
                    metrics.get("score_improvement"),

                "pass_count":
                    metrics.get("pass_count"),

                "revise_count":
                    metrics.get("revise_count"),

                "final_verdict":
                    metrics.get("final_verdict"),

                "report_word_count":
                    metrics.get("report_word_count"),

                "actual_run_time_seconds":
                    round(run_time, 2),
            }

            results.append(result)

            print("\nRun completed successfully.")

            print(
                f"Final score: "
                f"{result['final_critic_score']}/10"
            )

            print(
                f"Revisions: "
                f"{result['revisions']}"
            )

            print(
                f"Latency: "
                f"{result['latency_seconds']} sec"
            )

        except Exception as e:

            run_time = time.perf_counter() - run_start

            print("\nRUN FAILED")
            print(f"Error: {e}")

            results.append({
                "run_id": index,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),

                "status": "FAILED",

                "error": str(e),

                "actual_run_time_seconds":
                    round(run_time, 2),
            })

    total_time = time.perf_counter() - total_start

    return results, total_time


# ============================================================
# Calculate aggregate metrics
# ============================================================

def calculate_summary(results, total_time):

    successful_runs = [
        r for r in results
        if r.get("status") == "SUCCESS"
    ]

    failed_runs = [
        r for r in results
        if r.get("status") == "FAILED"
    ]

    if not successful_runs:

        return {
            "total_topics": len(results),
            "successful_runs": 0,
            "failed_runs": len(failed_runs),
        }

    # --------------------------------------------------------
    # Helper
    # --------------------------------------------------------

    def average(field):

        values = [
            r[field]
            for r in successful_runs
            if r.get(field) is not None
        ]

        if not values:
            return None

        return round(
            sum(values) / len(values),
            2
        )

    # --------------------------------------------------------
    # Scores
    # --------------------------------------------------------

    first_scores = [
        r["first_critic_score"]
        for r in successful_runs
        if r.get("first_critic_score") is not None
    ]

    final_scores = [
        r["final_critic_score"]
        for r in successful_runs
        if r.get("final_critic_score") is not None
    ]

    score_improvements = [
        r["score_improvement"]
        for r in successful_runs
        if r.get("score_improvement") is not None
    ]

    # --------------------------------------------------------
    # Pass rate
    # --------------------------------------------------------

    passed = sum(
        r.get("final_verdict") == "PASS"
        for r in successful_runs
    )

    pass_rate = round(
        (passed / len(successful_runs)) * 100,
        2
    )

    # --------------------------------------------------------
    # Revision statistics
    # --------------------------------------------------------

    revision_values = [
        r["revisions"]
        for r in successful_runs
        if r.get("revisions") is not None
    ]

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = {

        "benchmark_timestamp":
            datetime.now().isoformat(),

        "total_topics":
            len(results),

        "successful_runs":
            len(successful_runs),

        "failed_runs":
            len(failed_runs),

        "success_rate_percent":
            round(
                (
                    len(successful_runs)
                    / len(results)
                ) * 100,
                2
            ) if results else 0,

        "total_benchmark_time_seconds":
            round(total_time, 2),

        # --------------------------------------------
        # Quality
        # --------------------------------------------

        "average_first_critic_score":
            round(
                sum(first_scores) / len(first_scores),
                2
            ) if first_scores else None,

        "average_final_critic_score":
            round(
                sum(final_scores) / len(final_scores),
                2
            ) if final_scores else None,

        "average_score_improvement":
            round(
                sum(score_improvements)
                / len(score_improvements),
                2
            ) if score_improvements else None,

        "best_final_score":
            max(final_scores)
            if final_scores else None,

        "worst_final_score":
            min(final_scores)
            if final_scores else None,

        # --------------------------------------------
        # Revision
        # --------------------------------------------

        "average_revisions":
            round(
                sum(revision_values)
                / len(revision_values),
                2
            ) if revision_values else None,

        "max_revisions":
            max(revision_values)
            if revision_values else None,

        # --------------------------------------------
        # Sources
        # --------------------------------------------

        "average_search_sources":
            average("search_sources"),

        "average_scraped_sources":
            average("scraped_sources"),

        "average_source_utilization_percent":
            average(
                "source_utilization_percent"
            ),

        # --------------------------------------------
        # Report
        # --------------------------------------------

        "average_report_word_count":
            average("report_word_count"),

        # --------------------------------------------
        # Performance
        # --------------------------------------------

        "average_latency_seconds":
            average("latency_seconds"),

        "min_latency_seconds":
            min(
                r["latency_seconds"]
                for r in successful_runs
                if r.get("latency_seconds") is not None
            ),

        "max_latency_seconds":
            max(
                r["latency_seconds"]
                for r in successful_runs
                if r.get("latency_seconds") is not None
            ),

        # --------------------------------------------
        # Final verdict
        # --------------------------------------------

        "pass_rate_percent":
            pass_rate,
    }

    return summary


# ============================================================
# Save JSON
# ============================================================

def save_json(results, summary):

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    with open(
        SUMMARY_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# Save CSV
# ============================================================

def save_csv(results):

    if not results:
        return

    fieldnames = set()

    for result in results:
        fieldnames.update(
            result.keys()
        )

    fieldnames = sorted(fieldnames)

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)


# ============================================================
# Print summary
# ============================================================

def print_summary(summary):

    print("\n")
    print("=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    print(
        f"\nTopics tested: "
        f"{summary['total_topics']}"
    )

    print(
        f"Successful runs: "
        f"{summary['successful_runs']}"
    )

    print(
        f"Failed runs: "
        f"{summary['failed_runs']}"
    )

    print(
        f"Success rate: "
        f"{summary['success_rate_percent']}%"
    )

    print("\nQUALITY")

    print(
        f"Average first critic score: "
        f"{summary['average_first_critic_score']}/10"
    )

    print(
        f"Average final critic score: "
        f"{summary['average_final_critic_score']}/10"
    )

    print(
        f"Average score improvement: "
        f"+{summary['average_score_improvement']}"
    )

    print(
        f"Best final score: "
        f"{summary['best_final_score']}/10"
    )

    print(
        f"Worst final score: "
        f"{summary['worst_final_score']}/10"
    )

    print("\nREVISION")

    print(
        f"Average revisions: "
        f"{summary['average_revisions']}"
    )

    print(
        f"Maximum revisions: "
        f"{summary['max_revisions']}"
    )

    print("\nSOURCES")

    print(
        f"Average search sources: "
        f"{summary['average_search_sources']}"
    )

    print(
        f"Average scraped sources: "
        f"{summary['average_scraped_sources']}"
    )

    print(
        f"Average source utilization: "
        f"{summary['average_source_utilization_percent']}%"
    )

    print("\nPERFORMANCE")

    print(
        f"Average latency: "
        f"{summary['average_latency_seconds']} sec"
    )

    print(
        f"Minimum latency: "
        f"{summary['min_latency_seconds']} sec"
    )

    print(
        f"Maximum latency: "
        f"{summary['max_latency_seconds']} sec"
    )

    print(
        f"Average report size: "
        f"{summary['average_report_word_count']} words"
    )

    print(
        f"\nFinal PASS rate: "
        f"{summary['pass_rate_percent']}%"
    )

    print("\n")
    print("=" * 70)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    results, total_time = run_benchmark(TOPICS)

    summary = calculate_summary(
        results,
        total_time
    )

    save_json(
        results,
        summary
    )

    save_csv(results)

    print_summary(summary)

    print("\nFiles created:")

    print(f"  {OUTPUT_JSON}")
    print(f"  {OUTPUT_CSV}")
    print(f"  {SUMMARY_JSON}")
