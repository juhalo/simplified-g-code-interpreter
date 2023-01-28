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
    read_file_to_list(filename, machine)

def read_file_to_list(filename: str, machine_name: MachineClient) -> list:
  """Reading file to list allows to check and not "execute" an incorrectly formatted or otherwise incorrect file"""
  try:
    rows_list = []
    with open(filename, 'r') as f:
        for line in f:
          stripped_line = line.strip()
          if len(stripped_line) != 0:
            rows_list.append(stripped_line)
    print(rows_list)
    rows_list
  except FileNotFoundError:
    print("File '{}' was not found.".format(filename))
  except PermissionError:
    print("The program does not have permission to access the file '{}'.".format(filename))

if __name__ == "__main__":
  try:
    # Import sys here which allows us to use the program as a library without causing import errors, could have put it to top like a normal person
    import sys
    file = sys.argv[1]
    main(file)
  except ImportError:
    print("The Python module 'sys' was not found.")
