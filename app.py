import streamlit as st

from pipeline import run_research_pipeline


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Multi-Agent Research System")

st.write(
    "Enter a research topic and let the multi-agent "
    "pipeline search, read, write and critique the report."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    max_revisions = st.slider(
        "Maximum revisions",
        min_value=0,
        max_value=5,
        value=1
    )

    st.info(
        "Pipeline:\n\n"
        "🔎 Search Agent\n\n"
        "📖 Reader Agent\n\n"
        "✍️ Writer Agent\n\n"
        "🧐 Critic Agent"
    )


# --------------------------------------------------
# Topic input
# --------------------------------------------------

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Impact of AI on software engineering"
)


# --------------------------------------------------
# Run button
# --------------------------------------------------

if st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True
):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        # ----------------------------------------------
        # Load pipeline
        # ----------------------------------------------

        status = st.empty()
        progress = st.progress(0)

        status.info("🔧 Loading research pipeline...")
        progress.progress(5)

        try:

            # Import only after the user starts the research.
            from pipeline import run_research_pipeline

        except Exception as e:

            progress.empty()

            status.error(
                "❌ Could not load the research pipeline."
            )

            st.error(
                "There is an error in one of the pipeline files."
            )

            with st.expander("🔍 Show technical error"):

                st.exception(e)

            st.stop()

        # ----------------------------------------------
        # Start pipeline
        # ----------------------------------------------

        status.info("🔎 Starting research pipeline...")
        progress.progress(10)

        try:

            result = run_research_pipeline(
                topic.strip(),
                max_revisions=max_revisions,
            )

            progress.progress(100)

            status.success(
                "✅ Research completed successfully!"
            )

        except Exception as e:

            progress.empty()

            status.error(
                "❌ Research pipeline failed."
            )

            with st.expander(
                "🔍 Show technical error",
                expanded=True,
            ):

                st.exception(e)

            st.stop()

        # ==================================================
        # RESULTS
        # ==================================================

        st.divider()

        st.header("📄 Research Report")

        report = result.get(
            "report",
            "No report generated.",
        )

        if report:

            st.markdown(report)

        else:

            st.warning(
                "No report was generated."
            )

        # ==================================================
        # METRICS
        # ==================================================

        st.divider()

        st.header("📊 Metrics")

        metrics = result.get(
            "metrics",
            {},
        )

        # ----------------------------------------------
        # First row of metrics
        # ----------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            final_score = metrics.get(
                "final_critic_score",
                "N/A",
            )

            st.metric(
                "Critic Score",
                f"{final_score}/10",
            )

        with col2:

            st.metric(
                "Revisions",
                metrics.get(
                    "revisions",
                    "N/A",
                ),
            )

        with col3:

            st.metric(
                "Sources",
                metrics.get(
                    "search_sources",
                    "N/A",
                ),
            )

        with col4:

            latency = metrics.get(
                "latency_seconds",
                "N/A",
            )

            st.metric(
                "Latency",
                f"{latency} sec",
            )

        # ----------------------------------------------
        # Second row of metrics
        # ----------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Sources Scraped",
                metrics.get(
                    "scraped_sources",
                    "N/A",
                ),
            )

        with col2:

            first_score = metrics.get(
                "first_critic_score",
                "N/A",
            )

            st.metric(
                "First Score",
                f"{first_score}/10",
            )

        with col3:

            improvement = metrics.get(
                "score_improvement",
                0,
            )

            st.metric(
                "Score Improvement",
                f"+{improvement}",
            )

        with col4:

            st.metric(
                "Report Words",
                metrics.get(
                    "report_word_count",
                    "N/A",
                ),
            )

        # ==================================================
        # RESEARCH SOURCES
        # ==================================================

        st.divider()

        st.header("🔗 Research Sources")

        search_results = result.get(
            "search_results",
            "",
        )

        if search_results:

            st.text(search_results)

        else:

            st.info(
                "No search results available."
            )

        # ==================================================
        # CRITIC FEEDBACK
        # ==================================================

        st.divider()

        st.header("🧐 Critic Feedback")

        feedback = result.get(
            "feedback",
            "",
        )

        if feedback:

            st.text(feedback)

        else:

            st.info(
                "No critic feedback available."
            )