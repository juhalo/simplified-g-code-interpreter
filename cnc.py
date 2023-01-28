class MachineClient:

  def home(self):
    """ Moves machine to home position. """
    print("Moving to home.")

  def move(self, x, y, z):
    """ Uses linear movement to move spindle to given XYZ
    coordinates.
    Args:
    x (float): X axis absolute value [mm]
    y (float): Y axis absolute value [mm]
    z (float): Z axis absolute value [mm]
    """
    print("Moving to X={:.3f} Y={:.3f} Z={:.3f} [mm].".format(x, y,
    z))

  def move_x(self, value):
    """ Move spindle to given X coordinate. Keeps current Y and Z
    unchanged.
    Args:
    value (float): Axis absolute value [mm]
    """
    print("Moving X to {:.3f} [mm].".format(value))

  def move_y(self, value):
    """ Move spindle to given Y coordinate. Keeps current X and Z
    unchanged.
    Args:
    value(float): Axis absolute value [mm]
    """
    print("Moving Y to {:.3f} [mm].".format(value))

  def move_z(self, value):
    """ Move spindle to given Z coordinate. Keeps current X and Y
    unchanged.
    Args:
    value (float): Axis absolute value [mm]
    """
    print("Moving Z to {:.3f} [mm].".format(value))

  def set_feed_rate(self, value):
    """ Set spindle feed rate.
    Args:
    value (float): Feed rate [mm/s]
    """
    print("Using feed rate {} [mm/s].".format(value))

  def set_spindle_speed(self, value):
    """ Set spindle rotational speed.
    Args:
    value (int): Spindle speed [rpm]
    """
    print("Using spindle speed {} [mm/s].".format(value))

  def change_tool(self, tool_name):
    """ Change tool with given name.
    Args:
    tool_name (str): Tool name.
    """
    print("Changing tool '{:s}'.".format(tool_name))

  def coolant_on(self):
    """ Turns spindle coolant on. """
    print("Coolant turned on.")

  def coolant_off(self):
    """ Turns spindle coolant off. """
    print("Coolant turned off.")

def main(filename: str) -> None:
    machine = MachineClient()
    line_list = read_file_to_list(filename, machine)
    print(line_list)
    if len(line_list) > 0:
      correct_format = check_lines(line_list)
      if correct_format:
        line_list = line_list[2:-1]
      print(correct_format)
      print(line_list)

def read_file_to_list(filename: str, machine_name: MachineClient) -> list:
  """Reading file to list allows to check and not "execute" an incorrectly formatted or otherwise incorrect file"""
  try:
    rows_list = []
    with open(filename, 'r') as f:
        for line in f:
          stripped_line = line.strip()
          if len(stripped_line) != 0:
            rows_list.append(stripped_line)
  except FileNotFoundError:
    print("File '{}' was not found.".format(filename))
  except PermissionError:
    print("The program does not have permission to access the file '{}'.".format(filename))
  finally:
    return rows_list

def check_lines(lines: list) -> bool:
  if not correct_start_or_end(lines[0]) or not correct_start_or_end(lines[-1]):
    return False
  if not correct_program_number(lines[1]):
    return False
  return True

def correct_start_or_end(line: str) -> bool:
  """"Allows start and end lines to have a comment after the '%' sign"""
  if line[0] != "%":
    return False
  if len(line.strip()) > 1:
    potential_comment = line[1:].strip()
    if potential_comment[0] != "(":
      return False
    if potential_comment[-1] != ")":
      return False
  return True

def correct_program_number(line: str) -> bool:
  """"Has to start with a big 'O' followed by four digits and can have a comment"""
  if line[0] != "O" or len(line) < 5:
    return False
  digits_string = "0123456789"
  for i in range(1, 5):
    if line[i] not in digits_string:
      return False
  if len(line) > 5:
    potential_comment = line[5:].strip()
    if potential_comment[0] != "(":
      return False
    if potential_comment[-1] != ")":
      return False
  return True

if __name__ == "__main__":
  try:
    # Import sys here which allows us to use the program as a library without causing import errors, could have put it to top like a normal person
    import sys
    file = sys.argv[1]
    main(file)
  except ImportError:
    print("The Python module 'sys' was not found.")
