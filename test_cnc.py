from cnc import MachineClient
from cnc_exceptions import SourceFileFormatError
import cnc
import pytest

def test_full_rectangle() -> None:
  """"Test execution of correctly loading and executing correct rectangle.gcode file"""
  machine = MachineClient()
  machine.home() # Assume that at the beginning of the program go to home
  machine.print_coords()
  filename = 'rectangle.gcode'
  print()
  i = 0
  correct_values = {
    "rapid": [False, True, True, True, True, False, False, False, False, False, False, True, True, True],
    "linear": [False, False, False, False, False, True, True, True, True, True, True, False, False, False],
    "feed": [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0],
    "speed": [0, 0, 0, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 0, 0],
    "coolant": [False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "rot": [False, False, False, True, True, True, True, True, True, True, True, True, False, False],
    "tool": ["", "", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1"],
    "mm": [None, True, True, True, True, True, True, True, True, True, True, True, True, True],
    "plane": ["", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY"],
    "x": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -12.000, 110.000, 110.000, -10.000, -10.000, -10.000, 0.000, 0.000],
    "y": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -10.000, -10.000, 210.000, 210.000, -12.000, -12.000, 0.000, 0.000],
    "z": [0.0, 0.0, 0.0, 0.0, 0.0, -5.000, -5.000, -5.000, -5.000, -5.000, -5.000, 10.000, 0.000, 0.000]
    }
  assert machine._rapid_movement == correct_values["rapid"][i]
  assert machine._linear_movement == correct_values["linear"][i]
  assert machine._feed_rate == correct_values["feed"][i]
  assert machine._spindle_speed == correct_values["speed"][i]
  assert machine._coolant_on == correct_values["coolant"][i]
  assert machine._rot_on == correct_values["rot"][i]
  assert machine._tool == correct_values["tool"][i]
  assert machine._use_mm == correct_values["mm"][i]
  assert machine._plane == correct_values["plane"][i]
  assert machine._x == correct_values["x"][i]
  assert machine._y == correct_values["y"][i]
  assert machine._z == correct_values["z"][i]
  i += 1
  line_list = cnc.read_file_to_list(filename)
  cnc.check_start_and_end(line_list)
  line_list = line_list[2:-1]
  line_list = cnc.remove_comments(line_list)
  for line in line_list:
    machine.execute_line(line)
    assert machine._rapid_movement == correct_values["rapid"][i]
    assert machine._linear_movement == correct_values["linear"][i]
    assert machine._feed_rate == correct_values["feed"][i]
    assert machine._spindle_speed == correct_values["speed"][i]
    assert machine._coolant_on == correct_values["coolant"][i]
    assert machine._rot_on == correct_values["rot"][i]
    assert machine._tool == correct_values["tool"][i]
    assert machine._use_mm == correct_values["mm"][i]
    assert machine._plane == correct_values["plane"][i]
    assert machine._x == correct_values["x"][i]
    assert machine._y == correct_values["y"][i]
    assert machine._z == correct_values["z"][i]
    i += 1

def test_different_movements() -> None:
  """Tests moving in all of the different ways."""
  machine = MachineClient()
  machine.home()
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', 'N15 X20.000 Y-5.000 Z-10.000', 'N16 Y-6.00 Z-11.000', 'N17 X19.000 Z-10.000', 'N18', '(LIFT SPINDLE)', 'N19 G00 Z10.000 M09',
  'N20 X5.000 Y25.000 Z5.000', 'N21 X0.000', 'N22 Y2.000', 'N23 Y5.000 Z2.000', 'N24 X3.000 Z1.000', 'N25 X-20.000 Y2.000',
  'N26 Y-20.000 Z5.000', 'N27 X-25.000 Z2.000', 'N28 Y5.000 Z5.000', 'N29 X-5.000 Y2.000', 'N30  X-3.000 Y-5.000 F300. M08',
  'N31 Y-3.000 Z-5.000', 'N32 X-4.000 Z-10.000', 'N33 Y-4.000 Z1.000', 'N34 X-3.000 Z6.000', 'N35 X-2.000 Z7.000',
  '(STOP SPINDLE)', 'N36 G91 G28 G20 G19 Z0.0 M05', '(PROGRAM END)', 'N38 G18 M30', '%']
  i = 0
  correct_values = {
    "rapid": [False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, True, True,
              True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    "linear": [False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "feed": [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0,
            600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0],
    "speed": [0, 0, 0, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,
              2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 0, 0],
    "coolant":  [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True],
    "rot":      [False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True, True, True, True, True, False, False],
    "tool": ["", "", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1",
            "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1",
            "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1"],
    "mm": [None, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
          True, True, True, True, True, True, True, True, True, True, True, True, False, False],
    "plane": ["", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY",
              "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "YZ", "ZX"],
    "x": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -12.000, 110.000, 110.000, -10.000, -10.000, 20.000, 20.000, 19.000, 19.000, 19.000,
          5.000, 0.000, 0.000, 0.000, 3.000, -20.000, -20.000, -25.000, -25.000, -5.000, -3.000, -3.000, -4.000, -4.000, -3.000, -2.000,
          0.000, 0.000],
    "y": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -10.000, -10.000, 210.000, 210.000, -12.000, -5.000, -6.000, -6.000, -6.000, -6.000, 25.000,
          25.000, 2.000, 5.000, 5.000, 2.000, -20.000, -20.000, 5.000, 2.000, -5.000, -3.000, -3.000, -4.000, -4.000, -4.000, 0.000,
          0.000],
    "z": [0.0, 0.0, 0.0, 0.0, 0.0, -5.000, -5.000, -5.000, -5.000, -5.000, -5.000, -10.000, -11.000, -10.000, -10.000, 10.000, 5.000, 5.000,
          5.000, 2.000, 1.000, 1.000, 5.000, 2.000, 5.000, 5.000, 5.000, -5.000, -10.000, 1.000, 6.000, 7.000, 0.000, 0.000]
    }
  assert machine._rapid_movement == correct_values["rapid"][i]
  assert machine._linear_movement == correct_values["linear"][i]
  assert machine._feed_rate == correct_values["feed"][i]
  assert machine._spindle_speed == correct_values["speed"][i]
  assert machine._coolant_on == correct_values["coolant"][i]
  assert machine._rot_on == correct_values["rot"][i]
  assert machine._tool == correct_values["tool"][i]
  assert machine._use_mm == correct_values["mm"][i]
  assert machine._plane == correct_values["plane"][i]
  assert machine._x == correct_values["x"][i]
  assert machine._y == correct_values["y"][i]
  assert machine._z == correct_values["z"][i]
  i += 1
  cnc.check_start_and_end(line_list)
  line_list = line_list[2:-1]
  line_list = cnc.remove_comments(line_list)
  for line in line_list:
    machine.execute_line(line)
    assert machine._rapid_movement == correct_values["rapid"][i]
    assert machine._linear_movement == correct_values["linear"][i]
    assert machine._feed_rate == correct_values["feed"][i]
    assert machine._spindle_speed == correct_values["speed"][i]
    assert machine._coolant_on == correct_values["coolant"][i]
    assert machine._rot_on == correct_values["rot"][i]
    assert machine._tool == correct_values["tool"][i]
    assert machine._use_mm == correct_values["mm"][i]
    assert machine._plane == correct_values["plane"][i]
    assert machine._x == correct_values["x"][i]
    assert machine._y == correct_values["y"][i]
    assert machine._z == correct_values["z"][i]
    i += 1

def test_incorrect_file_name() -> None:
  with pytest.raises(FileNotFoundError):
    cnc.main("reactangle.gcode")

def test_call_main_function() -> None:
  """Tests whether or not calling main function with correct file causes an error"""
  try:
    cnc.main("rectangle.gcode")
  except:
    assert False

def test_incorrect_first_line() -> None:
  line_list = ['%%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect first line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_first_line_two() -> None:
  line_list = ['(%)' ,'%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect first line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_last_line() -> None:
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect final line"):
    cnc.check_start_and_end(line_list)

def test_commented_first_line() -> None:
  line_list = ['%(Hello, there)', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  try:
     cnc.check_start_and_end(line_list)
  except SourceFileFormatError as _:
    assert False

def test_unclosed_first_line_comment() -> None:
  line_list = ['%(Hau', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect first line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_program_number_line() -> None:
  line_list = ['%', 'OO001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)


def test_program_number_line_too_short() -> None:
  line_list = ['%', 'O001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_program_number_line_too_long() -> None:
  line_list = ['%', 'O00001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_unclosed_comment_program_number() -> None:
  line_list = ['%', 'O0001(', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_program_number_line_three() -> None:
  """"Test that checks that program is not run if the first character of program line is not 'O'"""
  line_list = ['%', '0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_closed_command_line_comment() -> None:
  line = 'N6 G90 G54 G00 X-12.000 Y-12.000 (/Hello)'
  assert cnc.correct_line(line) == True

def test_command_line_invalid_char() -> None:
  line = 'N6 G90 G54 G00 X-12.000 Y-12.000 K9 / Hehhe%(/{[  d'
  assert cnc.correct_line(line) == False

def test_command_no_command() -> None:
  line = 'N6 G90 G54 G00 X-12.000 Y-12.000 99'
  assert cnc.correct_line(line) == False

def test_command_too_many_commands() -> None:
  line = 'N6 G90 G54 G00 X-12.000 Y-12.000 YY9'
  assert cnc.correct_line(line) == False

def test_command_without_number() -> None:
  line = 'N6 G90 G54 G00 X-12.000 Y-12.000 Y'
  assert cnc.correct_line(line) == False

def test_unclosed_command_line_comment() -> None:
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_unopened_command_line_comment() -> None:
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_commenting_with_slashes() -> None:
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', '/N10 G01jhdjkshf&%#"@)()=]} X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_no_movement_type() -> None:
  """"Tests that if no movement type is specified at all before the move command, throws an error."""
  machine = MachineClient()
  line_list = ['N1 G17 G21 G40 G49 G80 G94', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 X-12.000 Y-12.000','N9 G01 Z-5.000 F100.',
  'N10 G01 X-12.000 Y-10.000 Q600.', 'N11 G01 X110.000', 'N12 G01 Y210.000', 'N13 G01 X-10.000', 'N14 G01 Y-12.000', 'N15 G00 Z10.000 M09',
  'N16 G91 G28 Z0.0 M05', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Movement type not defined"):
    for line in line_list:
      machine.execute_line(line)

def test_no_feed_rate() -> None:
  """"Tests that if feed rate is zero and tries to move, throws an error."""
  machine = MachineClient()
  machine.home()
  line_list = ['N1 G00 G17 G21 G40 G49 G80 G94', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000','N9 G01 Z-5.000',
  'N10 G01 X-12.000 Y-10.000 Q600.', 'N11 G01 X110.000', 'N12 G01 Y210.000', 'N13 G01 X-10.000', 'N14 G01 Y-12.000', 'N15 G00 Z10.000 M09',
  'N16 G91 G28 Z0.0 M05', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Cannot execute movement due to feed rate being 0"):
    for line in line_list:
      machine.execute_line(line)
