class Job:
    pass

class commonJob(Job):
    def __init__(self,capture_action,parse_action,save_action):
        self.capture_action = capture_action
        self.parse_action = parse_action
        self.save_action = save_action
    def run(self):
        capture_ret = self.capture_action.run()
        parse_ret = self.parse_action.run(capture_ret)
        save_ref = self.save_action.run(parse_ret)
