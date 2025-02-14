

class Utils:
    
    def __init__(self):
        pass

    def calculate_center_click(self, bounds):
        try:
            bounds = bounds.strip("[]").split("][")
            if len(bounds) != 2:
                raise ValueError("Bounds string format is incorrect. Expected format: '[x1,y1][x2,y2]'")
 
            x1, y1 = map(int, bounds[0].split(","))
            x2, y2 = map(int, bounds[1].split(","))
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
        except Exception as e:
            raise ValueError(f"Error calculating center: {e}")