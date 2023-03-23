from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from collatz_activity import collatz, graph


@workflow.defn
class CollatzWorkflow:
    @workflow.run
    async def run(self, number):
        results = await workflow.execute_activity(
            collatz,
            number,
            start_to_close_timeout=timedelta(seconds=10),
        )
        num_list = results[0]
        await workflow.execute_activity(
            graph,
            num_list,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return results
