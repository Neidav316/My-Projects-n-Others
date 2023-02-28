extends Button

onready var anim_player: AnimationPlayer = $AnimationPlayer


func _on_button_up():
	anim_player.play("Fade_Black")
	yield(anim_player, "animation_finished")
	get_tree().paused = false
	get_tree().reload_current_scene()
