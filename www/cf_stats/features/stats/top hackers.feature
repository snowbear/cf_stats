Feature: "Top hackers" stats

  Scenario: Basic test
    Given contest standings
      | party    | hacks+ | hacks- |
      | hacker 1 | 3      | 0      |
      | hacker 2 | 2      | 0      |
      | hacker 3 | 1      | 0      |

    Then "Top hackers" stat should be
      | score | party    | hacks+ | hacks- |
      | 300   | hacker 1 | 3      | 0      |
      | 200   | hacker 2 | 2      | 0      |
      | 100   | hacker 3 | 1      | 0      |

  Scenario: they should be sorted correctly
    Given contest standings
      | party  | hacks+ | hacks- |
      | fourth | 1      | 0      |
      | third  | 2      | 2      |
      | second | 2      | 2      |
      | first  | 2      | 0      |

    Then "Top hackers" stat should be
      | score | party  |
      | 200   | first  |
      | 100   | second |
      | 100   | third  |
      | 100   | fourth |

  Scenario: should limit number of rows if scores are distinct
    Given contest standings
      | party | hacks+ | hacks- |
      | p1    | 6      | 0      |
      | p2    | 5      | 0      |
      | p3    | 4      | 0      |
      | p4    | 3      | 0      |
      | p5    | 2      | 0      |
      | p6    | 1      | 0      |

    Then "Top hackers" stat should contain 5 rows

  Scenario: should show more rows if there is a tie in scores
    Given contest standings
      | party | hacks+ |
      | p1    | 4      |
      | p2    | 4      |
      | p3    | 3      |
      | p4    | 3      |
      | p5    | 2      |
      | p6    | 2      |
      | p7    | 1      |

    Then "Top hackers" stat should contain 6 rows

  Scenario: should limit number of rows even in case of ties
    Given contest standings
      | party | hacks+ |
      | p1    | 1      |
      | p2    | 1      |
      | p3    | 1      |
      | p4    | 1      |
      | p5    | 1      |
      | p6    | 1      |
      | p7    | 1      |
      | p8    | 1      |
      | p9    | 1      |
      | p10   | 1      |
      | p11   | 1      |

    Then "Top hackers" stat should contain 10 rows

  Scenario: hackers with negative and zero score should not be shown
    Given contest standings
      | party | hacks+ | hacks- |
      | p1    | 1      | 0      |
      | p2    | 1      | 2      |
      | p3    | 0      | 0      |
      | p4    | 1      | 3      |

    Then "Top hackers" stat should be
      | party |
      | p1    |