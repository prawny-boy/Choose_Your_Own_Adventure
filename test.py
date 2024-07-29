from sys import exit

class CounterExceededError(Exception):
    """Exception raised when the input attempt counter exceeds the allowed limit."""
    def __init__(self, message="Input attempt counter exceeded the allowed limit."):
        self.message = message
        super().__init__(self.message)

def LimitedInput(Question="Input here: ", Options=["yes", "no"], FailedOutput="That is not a valid option. Please try again.", TryAgainMessage=True, ListOptions=True, CounterNumber=0, AllowQuit=True):
    Counter = 1
    if AllowQuit:
        Options.append("quit")
    DisplayOptions = "; ".join(Options).upper()
    while True:
        print(Question)
        if ListOptions:
            print(f"Options: {DisplayOptions}.")
        UserInput = input(": ").strip().lower()
        if UserInput in Options:
            if UserInput == "quit":
                exit()
            return UserInput
        elif Counter == CounterNumber:
            raise CounterExceededError("Maximum number of attempts exceeded.")
        else:
            if TryAgainMessage:
                print(FailedOutput)
    
        if CounterNumber > 0: Counter += 1

while True:
    playerState = "a"
    if playerState == "a":
        print("bald a")
        playerState = LimitedInput(Question="Which house? ", Options=["c", "b"])
    if playerState == "b":
        print("bald b")
        playerState = LimitedInput(Question="Which house? ", Options=["a", "c"])
    if playerState == "c":
        print("bald c")
        playerState = LimitedInput(Question="Which house? ", Options=["a", "b"])
    else:
        print("in the quiet misty morning")