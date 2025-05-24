# Basic conditional logic plugin

def run_if_else(condition, true_action, false_action):
    if condition:
        return true_action()
    else:
        return false_action()
