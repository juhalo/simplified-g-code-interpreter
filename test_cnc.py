from cnc import MachineClient
from cnc_exceptions import SourceFileFormatError
import cnc
import pytest

def test_correct_full_rectangle():
  machine = MachineClient()
  machine.home()
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
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
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

def test_correct_expanded_rectangle():
  """Tests moving all three coordinates linearly and rapidly and that linear/rapid movement does not change unless specified."""
  machine = MachineClient()
  machine.home()
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', 'N15 X20.000 Y-5.000 Z-10.000', '(LIFT SPINDLE)', 'N16 G00 Z10.000 M09', 'N17 X5.000 Y25.000 Z5.000', '(STOP SPINDLE)', 'N18 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N20 M30', '%']
  i = 0
  correct_values = {
    "rapid": [False, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True],
    "linear": [False, False, False, False, False, True, True, True, True, True, True, True, False, False, False, False],
    "feed": [0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0],
    "speed": [0, 0, 0, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 0, 0],
    "coolant": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    "rot": [False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False],
    "tool": ["", "", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1", "Tool 1"],
    "mm": [None, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    "plane": ["", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY", "XY"],
    "x": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -12.000, 110.000, 110.000, -10.000, -10.000, 20.000, 20.000, 5.000, 0.000, 0.000],
    "y": [0.0, 0.0, 0.0, 0.0, -12.000, -12.000, -10.000, -10.000, 210.000, 210.000, -12.000, -5.000, -5.000, 25.000, 0.000, 0.000],
    "z": [0.0, 0.0, 0.0, 0.0, 0.0, -5.000, -5.000, -5.000, -5.000, -5.000, -5.000, -10.000, 10.000, 5.000, 0.000, 0.000]
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

def test_incorrect_file_name():
  with pytest.raises(FileNotFoundError):
    cnc.main("reactangle.gcode")

def test_incorrect_first_line():
  line_list = ['%%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect first line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_first_line_two():
  line_list = ['(%)' ,'%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect first line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_last_line():
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect final line"):
    cnc.check_start_and_end(line_list)

def test_commented_first_line():
  line_list = ['%(Hello, there)', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  try:
     cnc.check_start_and_end(line_list)
  except SourceFileFormatError as _:
    assert False

def test_incorrect_program_number_line():
  line_list = ['%', 'OO001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_incorrect_program_number_line_two():
  line_list = ['%', 'O001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  with pytest.raises(SourceFileFormatError, match=r"Incorrect program number line"):
    cnc.check_start_and_end(line_list)

def test_unclosed_command_line_comment():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_unopened_command_line_comment():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_invalid_character():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 Q600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_missing_command_line():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 6600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_too_many_commands():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 GG00.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_too_short_command():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)

def test_commenting_with_slashes():
  line_list = ['(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)',
  'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)',
  'N9 G01 Z-5.000 F100.', 'LINEAR FEED TO XY WITH GIVEN FEED RATE)', '/N10 G01jhdjkshf&%#"@)()=]} X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000',
  'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30']
  with pytest.raises(SourceFileFormatError, match=r"Problem in the command line"):
    cnc.remove_comments(line_list)
