tool
extends Button

onready var anim_player: AnimationPlayer = $AnimationPlayer

export(String, FILE) var next_scene_path: = ""

func _on_button_up():
	anim_player.play("Fade_Black")
	yield(anim_player, "animation_finished")
	get_tree().paused = false
	get_tree().change_scene(next_scene_path)

func _get_configuration_warning():
	return "next_scene_path needs to be set in order it to work" if not next_scene_path else ""
