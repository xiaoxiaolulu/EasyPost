from api.events.registry import G
from unitrunner.steps.base import BaseStep


@G.register("request")
class RequestStep(BaseStep):

    def setup(self):
        ...

    def run(self, **kwargs):
        ...

    def teardown(self):
        ...

    def run_test(self):
        """
        def run_step(step_type):
            step = G.get(step_type)
            step.run_test()
        """
        self.setup()
        self.run()
        self.teardown()
