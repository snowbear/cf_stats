Feature: CF data should be filtered and transformed appropriately when being loaded

  Scenario: Only submissions made by rated contestants should be left
    Given submissions for the contest
    | id | author |
    | 1  | a      |
    | 2  | b*     |
    | 3  | c#     |

    Then processed submissions should be like
    | id | author |
    | 1  | a      |

  Scenario: 1 # Enter scenario name here
    # Enter steps here