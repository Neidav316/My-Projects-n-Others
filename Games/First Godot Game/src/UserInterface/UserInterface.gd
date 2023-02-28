extends Control

onready var scene_tree: = get_tree()
onready var pause_overlay: ColorRect = get_node("PauseScreen")
onready var score: Label = get_node("Score")
onready var pause_title: Label = get_node("PauseScreen/PauseTitle")

var paused: = false setget set_paused
var can_click: = true

func _ready():
	PlayerData.connect("score_updated",self,"update_interface")
	PlayerData.connect("player_died",self,"_PlayerData_player_died")
	update_interface()

func _PlayerData_player_died():
	self.paused = true
	pause_title.text = "You Died"
	can_click = false
	

func _unhandled_input(event):
	if event.is_action_pressed("pause") and can_click:
		self.paused = !paused
		scene_tree.set_input_as_handled()

func set_paused(value: bool) -> void:
	paused = value
	scene_tree.paused = value
	pause_overlay.visible = value

func update_interface() -> void:
	score.text = "Score: %s" % PlayerData.score
