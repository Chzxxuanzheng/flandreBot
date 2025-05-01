class Button:
	def __init__(self, label: str, data: str, enter = True) -> None:
		self.label = label
		self.visited_label = label
		self.action_type = 2
		self.action_data = data
		self.action_reply = False
		self.action_enter = enter
		self.action_unsupport_tips = "此版本qq不支持"
		self.permisson_type = 2

	def toData(self)->dict:
		return {
          "render_data": {
            "label": self.label,
            "visited_label": self.visited_label
          },
          "action": {
            "type": self.action_type,
            "permission": {
              "type": self.permisson_type,
            },
            "unsupport_tips": self.action_unsupport_tips,
            "data": self.action_data,
			"enter": self.action_enter
          }
        }