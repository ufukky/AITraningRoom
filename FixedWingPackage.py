import time

def CratePayload(type = "",command="",info="",parameters = None):
    return {"type":type,"command":command,"info":info,"parameters":parameters,"signature":int(time.time() * 1000)}
