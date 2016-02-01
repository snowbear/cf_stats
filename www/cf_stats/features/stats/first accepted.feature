Feature: "First accepted" stats

  Scenario: nobody solved some problem
    Given submissions for the contest
    | problem | author | verdict      |
    | A       | looser | WRONG_ANSWER |

    Then "First accepted" stat should be like this
    | problem | time | authors |
    | A       |      |         |

  Scenario: single correct submission for problem
    Given submissions for the contest
    | problem | author | time  | verdict |
    | A       | first  | 00:05 | OK      |

    Then "First accepted" stat should be like this
    | problem | time  | authors |
    | A       | 00:05 | first   |

  Scenario: multiple correct submissions within a minute
    Given submissions for the contest
    | problem | author | time     | verdict |
    | A       | first  | 00:06:00 | OK      |
    | A       | second | 00:06:59 | OK      |

    Then "First accepted" stat should be like this
    | problem | time  | authors      |
    | A       | 00:06 | first second |

  Scenario: ignores incorrect submissions
    Given submissions for the contest
    | problem | author  | time  | verdict      |
    | A       | wrong   | 00:02 | WRONG_ANSWER |
    | A       | correct | 00:03 | OK           |

    Then "First accepted" stat should be like this
    | problem | time  | authors |
    | A       | 00:03 | correct |

  Scenario: multiple correct submissions are sorted correctly
    Given submissions for the contest
    | problem | author | time     | verdict |
    | A       | third  | 00:07:48 | OK      |
    | A       | first  | 00:07:13 | OK      |
    | A       | second | 00:07:48 | OK      |

    Then "First accepted" stat should be like this
    | problem | time  | authors            |
    | A       | 00:07 | first second third |

  Scenario: multiple problems
    Given submissions for the contest
    | problem | author | time  | verdict      |
    | A       | a1     | 00:02 | WRONG_ANSWER |
    | B       | b1     | 00:03 | OK           |
    | A       | a2     | 00:03 | OK           |
    | B       | b2     | 00:03 | WRONG_ANSWER |

    Then "First accepted" stat should be like this
    | problem | time  | authors |
    | A       | 00:03 | a2      |
    | B       | 00:03 | b1      |
