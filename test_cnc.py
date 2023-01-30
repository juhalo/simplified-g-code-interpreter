from cnc import MachineClient
import cnc
import pytest

def test_correct_full_rectangle():
  machine = MachineClient()
  machine.home()
  line_list = ['%', 'O0001', '(DIA 20.0 END MILL - NO CUTTER RADIUS COMP USED)', '(MACHINE OUTSIDE OF 100 X 200 RECTANGLE)', '(X0.0 Y0.0 - BOTTOM LEFT CORNER)', 'N1 G00 G17 G21 G40 G49 G80 G94', '(SET AND CHANGE TOOL 01)', 'N4 T01 M06', 'N5 S2000 M03', 'N6 G90 G54 G00 X-12.000 Y-12.000', '(CUTTING STARTS)', 'N9 G01 Z-5.000 F100.', '(LINEAR FEED TO XY WITH GIVEN FEED RATE)', 'N10 G01 X-12.000 Y-10.000 F600.', 'N11 G01 X110.000', 'N12 G01 Y210.000', 'N13 G01 X-10.000', 'N14 G01 Y-12.000', '(LIFT SPINDLE)', 'N15 G00 Z10.000 M09', '(STOP SPINDLE)', 'N16 G91 G28 Z0.0 M05', '(PROGRAM END)', 'N18 M30', '%']
  cnc.check_start_and_end(line_list)
  line_list = line_list[2:-1]
  line_list = cnc.remove_comments(line_list)
  for line in line_list:
    machine.execute_line(line)
  assert machine._x == 0.0
  assert machine._y == 0.0
  assert machine._z == 0.0
  assert machine._linear_movement == False
  assert machine._rapid_movement == True
  assert machine._rot_on == False
  assert machine._use_mm == True
