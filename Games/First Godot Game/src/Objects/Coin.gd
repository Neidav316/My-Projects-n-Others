extends Area2D

onready var anim_player: AnimationPlayer = get_node("AnimationPlayer")
export var score: = 100

func _on_Coin_body_entered(body):
	anim_player.play("Fade_Out")
	PlayerData.score += score	
