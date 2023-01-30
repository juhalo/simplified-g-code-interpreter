class MachineClient:
  def __init__(self):
    """Current implementation does not care about (all of) these initializations currently but might in the future"""
    self.__move_rapidly: bool = False
    self.__move_linearly: bool = False
    self.__feed_rate: float = 0
    self.__spindle_speed: int = 0
    self.__coolant_on: bool = False
    self.__rot_on: bool = False
    self.__tool: str = ""

  def home(self):
    """ Moves machine to home position. """
    self.__x: float = 0.0 # All are assumed to be zero
    self.__y: float = 0.0
    self.__z: float = 0.0
    print("Moving to home.")

  def print_coords(self):
    """"Prints current coordinates"""
    print("X={:.3f} Y={:.3f} Z={:.3f} [mm]".format(self.__x, self.__y, self.__z))

  def move(self, x, y, z):
    """ Uses linear movement to move spindle to given XYZ
    coordinates.
    Args:
    x (float): X axis absolute value [mm]
    y (float): Y axis absolute value [mm]
    z (float): Z axis absolute value [mm]
    """
    self.__x = x
    self.__y = y
    self.__z = z

    print("Moving to X={:.3f} Y={:.3f} Z={:.3f} [mm].".format(x, y,
    z))

  def move_rapid(self, x, y, z):
    """Moves machine along both axis defined and finish in
    one of these which has not completed. If only one axis
    is defined, currently calls move_'axis'
    Args:
    x (float): x axis absolute value [mm], can be None
    y (float): y axis absolute value [mm], can be None
    z (float): z axis absolute value [mm], can be None
    """
    if x == None and y == None and z == None:
      return
    if x == None and y == None:
      self.move_z(z)
    elif x == None and z == None:
      self.move_y(y)
    elif y == None and z == None:
      self.move_x(x)
    elif x == None:
      self.__move_two_rapidly(y, "y", z, "z", "x")
    elif y == None:
      self.__move_two_rapidly(x, "x", z, "z", "y")
    elif z == None:
      self.__move_two_rapidly(x, "x", y, "y", "z")
    else:
      self.__move_two_rapidly(x, "x", y, "y", "z")
      self.move_z(z)

  def __move_two_rapidly(self, axis_one: float, axis_one_name: str, axis_two: float, axis_two_name: str, axis_three_name: str):
    converter_dict = {"x": self.__x, "y": self.__y, "z": self.__z}
    current_axis_one = converter_dict[axis_one_name]
    current_axis_two = converter_dict[axis_two_name]
    axis_one_diff = axis_one - current_axis_one
    axis_two_diff = axis_two - current_axis_two
    if abs(axis_one_diff) > abs(axis_two_diff):
      if axis_one_diff < 0:
        if axis_three_name == "z":
          self.move(current_axis_one-abs(axis_two_diff), axis_two, self.__z)
        elif axis_three_name == "x":
          self.move(self.__x, current_axis_one-abs(axis_two_diff), axis_two)
        else:
          self.move(current_axis_one-abs(axis_two_diff), self.__y, axis_two)
        move_func_name = "move_" + axis_one_name
        move_func = getattr(self, move_func_name)
        move_func(axis_one)
      else:
        if axis_three_name == "z":
          self.move(current_axis_one+abs(axis_two_diff), axis_two, self.__z)
        elif axis_three_name == "x":
          self.move(self.__x, current_axis_one+abs(axis_two_diff), axis_two)
        else:
          self.move(current_axis_one+abs(axis_two_diff), self.__y, axis_two)
        move_func_name = "move_" + axis_one_name
        move_func = getattr(self, move_func_name)
        move_func(axis_one)
    elif abs(axis_one_diff) < abs(axis_two_diff):
      if axis_two_diff < 0:
        if axis_three_name == "z":
          self.move(axis_one, current_axis_two-abs(axis_one_diff), self.__z)
        elif axis_three_name == "x":
          self.move(self.__x, axis_one, current_axis_two-abs(axis_one_diff))
        else:
          self.move(axis_one, self.__y, current_axis_two-abs(axis_one_diff))
        move_func_name = "move_" + axis_two_name
        move_func = getattr(self, move_func_name)
        move_func(axis_one)
      else:
        if axis_three_name == "z":
          self.move(axis_one, current_axis_two+abs(axis_one_diff), self.__z)
        elif axis_three_name == "x":
          self.move(self.__x, axis_one, current_axis_two+abs(axis_one_diff))
        else:
          self.move(axis_one, self.__y, current_axis_two+abs(axis_one_diff))
        move_func_name = "move_" + axis_two_name
        move_func = getattr(self, move_func_name)
        move_func(axis_one)
    else:
      if axis_three_name == "z":
        self.move(axis_one, axis_two, self.__z)
      elif axis_three_name == "x":
        self.move(self.__x, axis_one, axis_two)
      else:
        self.move(axis_one, self.__y, axis_two)

  def move_linear(self, x, y, z):
    """Moves machine linearly to point (x,y,z)
    Args:
    x (float): x axis absolute value [mm], can be None
    y (float): y axis absolute value [mm], can be None
    z (float): z axis absolute value [mm], can be None
    """
    if x == None and y == None and z == None:
      return
    if x == None and y == None:
      self.move_z(z)
    elif x == None and z == None:
      self.move_y(y)
    elif y == None and z == None:
      self.move_x(x)
    elif x == None:
      self.move(self.__x, y, z)
    elif y == None:
      self.move(x, self.__y, z)
    elif z == None:
      self.move(x, y, self.__z)
    else:
      self.move(x, y, z)



  def move_x(self, value):
    """ Move spindle to given X coordinate. Keeps current Y and Z
    unchanged.
    Args:
    value (float): Axis absolute value [mm]
    """
    self.__x = value
    print("Moving X to {:.3f} [mm].".format(value))

  def move_y(self, value):
    """ Move spindle to given Y coordinate. Keeps current X and Z
    unchanged.
    Args:
    value(float): Axis absolute value [mm]
    """
    self.__y = value
    print("Moving Y to {:.3f} [mm].".format(value))

  def move_z(self, value):
    """ Move spindle to given Z coordinate. Keeps current X and Y
    unchanged.
    Args:
    value (float): Axis absolute value [mm]
    """
    self.__z = value
    print("Moving Z to {:.3f} [mm].".format(value))

  def set_feed_rate(self, value):
    """ Set spindle feed rate.
    Args:
    value (float): Feed rate [mm/s]
    """
    self.__feed_rate = value
    print("Using feed rate {} [mm/s].".format(value))

  def set_spindle_speed(self, value):
    """ Set spindle rotational speed.
    Args:
    value (int): Spindle speed [rpm]
    """
    self.__spindle_speed = value
    print("Using spindle speed {} [mm/s].".format(value))

  def spindle_rot_on(self):
    """ Turns spindle rotation on. """
    self.__rot_on = True
    print("Spindle rotation turned on.")

  def spindle_rot_off(self):
    """ Turns spindle rotation off. """
    self.__rot_on = False
    print("Spindle rotation turned on.")

  def change_tool(self, tool_name):
    """ Change tool with given name.
    Args:
    tool_name (str): Tool name.
    """
    self.__tool = tool_name
    print("Changing tool '{:s}'.".format(tool_name))

  def coolant_on(self):
    """ Turns spindle coolant on. """
    self.__coolant_on = True
    print("Coolant turned on.")

  def coolant_off(self):
    """ Turns spindle coolant off. """
    self.__coolant_on = False
    print("Coolant turned off.")

  def set_rapid_movement(self):
    """Sets the movement to rapid, can remain between lines"""
    if not self.__move_rapidly:
      self.__move_rapidly = True
      self.__move_linearly = False
      print("Change movement to rapid")

  def set_linear_movement(self):
    """"Sets the movement to linear, can remain between lines"""
    if not self.__move_linearly:
      self.__move_linearly = True
      self.__move_rapidly = False
      print("Change movement to linear")

  def execute_line(self, line):
    """ Execute the given line
    Args:
    line(str): Uncommented line of the .gcode file
    """
    x_move = None
    y_move = None
    z_move = None
    for command in line.split():
      if command[0] == "N":
        print(f"Line: {command}")
      elif command == "G0" or command == "G00":
        self.set_rapid_movement()
      elif command == "G01" or command == "G1":
        self.set_linear_movement()
      elif command == "G17":
        self.plane = "XY"
        print(f"Set plane to {self.plane}")
      elif command == "G18":
        self.plane = "ZX"
        print(f"Set plane to {self.plane}")
      elif command == "G19":
        self.plane = "YZ"
        print(f"Set plane to {self.plane}")
      elif command == "G20":
        self.__use_mm = False
        print("Use inches")
      elif command == "G21":
        self.__use_mm = True
        print("Use mm")
      elif command == "G28":
        self.home()
      elif command == "M3" or command == "M03":
        self.spindle_rot_on()
      elif command == "M4" or command == "M04":
        self.spindle_rot_off()
      elif command == "M5" or command == "M05":
        self.set_spindle_speed(0)
      elif command == "M8" or command == "M08":
        self.coolant_on()
      elif command == "M9" or command == "M09":
        self.coolant_off()
      elif command[0] == "S":
        self.set_spindle_speed(int(command[1:]))
      elif command[0] == "F":
        self.set_feed_rate(float(command[1:]))
      elif command[0] == "X":
        x_move = float(command[1:])
      elif command[0] == "Y":
        y_move = float(command[1:])
      elif command[0] == "Z":
        z_move = float(command[1:])
      elif command[0] == "T":
        self.change_tool(f"Tool {int(command[1:])}")
      else:
        print(f"Skipped: {command}")
    if self.__move_rapidly:
      self.move_rapid(x_move, y_move, z_move)
    elif self.__move_linearly:
      if self.__feed_rate == 0:
        print(f"Feed Rate is 0, cannot execute movement in (uncommented) line '{line}'")
        return False
      self.move_linear(x_move, y_move, z_move)
    else:
      print(f"On line '{line}' movement type not defined")
      return False

    self.print_coords()
    print()
    return True

def main(filename: str) -> None:
    machine = MachineClient()
    machine.home() # Assume that at the beginning of the program go to home
    machine.print_coords()
    print()
    line_list = read_file_to_list(filename, machine)
    if len(line_list) == 0:
      return
    correct_format = check_start_and_end(line_list)
    if not correct_format:
      return
    line_list = line_list[2:-1]
    line_list = remove_comments(line_list)
    if len(line_list) == 0:
        return
    for line in line_list:
      command_success = machine.execute_line(line)
      if not command_success:
        return

def read_file_to_list(filename: str, machine_name: MachineClient) -> list[str]:
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

def check_start_and_end(lines: list[str]) -> bool:
  if not correct_start_or_end(lines[0]) or not correct_start_or_end(lines[-1]):
    return False
  if not correct_program_number(lines[1]):
    return False
  return True

def correct_start_or_end(line: str) -> bool:
  """"Allows start and end lines to have a comment after the '%' sign"""
  if line[0] != "%":
    print("Does not start or end with '%'.")
    return False
  if len(line.strip()) > 1:
    potential_comment = line[1:].strip()
    if potential_comment[0] != "(":
      print("Incorrect characters in first or last line (line '{line}').")
      return False
    if potential_comment[-1] != ")":
      print("Incorrect characters in first or last line (line '{line}').")
      return False
  return True

def correct_program_number(line: str) -> bool:
  """"Has to start with a big 'O' followed by four digits and can have a comment"""
  if line[0] != "O":
    print("Program number does not start with 'O' or incorrect line in place of program number line.")
    return False
  if len(line) < 5:
    print("Program number line too short or incorrect line in place of program number line.")
    return False
  digits_string = "0123456789"
  for i in range(1, 5):
    if line[i] not in digits_string:
      print("Incorrect character in number part of program number or incorrect line in place of program number line.")
      return False
  if len(line) > 5:
    potential_comment = line[5:].strip()
    if potential_comment[0] != "(":
      print("Incorrect characters in program number line or incorrect comment.")
      return False
    if potential_comment[-1] != ")":
      print("Incorrect characters in program number line or incorrect comment.")
      return False
  return True

def remove_comments(lines: list[str]) -> list[str]:
  uncommented_lines = []
  for i in range(len(lines)):
    line = lines[i]
    if line[0] == "/" or ( line[0] == "(" and line[-1] == ")" ):
      continue
    if not correct_line(line):
      return []
    line = line.split("(")[0]
    line = line.split("/")[0] # Allows for everything after "/" to be skipped even when not in the beginning, this could be commented out
    uncommented_lines.append(line)
  return uncommented_lines

def correct_line(line: str) -> bool:
  if "(" in line:
    if line[-1] == ")":
      return True
    else:
      print(f"Comment not closed in line '{line}'.")
      return False
  elif ")" in line:
    return False
  splitted_line = line.split("/")[0] # We ignore all characters after the "/" sign
  accepted_chars = "0123456789NGXYZFSTMDEPC.- "
  for char in splitted_line:
    if char not in accepted_chars:
      print(f"Invalid character in line '{line}'.")
      return False
  commands = splitted_line.split() # It is assumed that spaces between commands are required, easy to change if needed
  for command in commands:
    if len(command) == 0:
      continue
    char_num = 0
    command_char = "NGXYZFSTMDEPC"
    for char in command_char:
      char_num += command.count(char)
    if char_num == 0:
      print(f"Missing command letter in a command in line '{line}'.")
      return False
    if char_num > 1:
      print(f"Too many command letters in a command in line '{line}'.")
      return False
    if len(command) == 1:
      print(f"Command too short in line '{line}'.")
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
