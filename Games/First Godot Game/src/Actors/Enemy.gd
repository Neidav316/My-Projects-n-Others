extends "res://src/Actors/Actor.gd"

onready var anim_player: AnimationPlayer = $AnimationPlayer

export var score: = 100

func _ready() -> void:
	set_physics_process(false)
	_velocity.x = -speed.x
	
func _on_StompDetector_body_entered(body: PhysicsBody2D) -> void:
	if body.global_position.y > get_node("StompDetector").global_position.y:
		return 
	set_physics_process(false)
	get_node("CollisionShape2D").disabled = true
	set_collision_layer_bit(2,false)
	get_node("StompDetector").set_collision_layer_bit(2,false)
	get_node("StompDetector").set_collision_mask_bit(1,false)
	anim_player.play("Death")
	yield(anim_player, "animation_finished")
	die()


func _physics_process(delta: float) -> void:
	_velocity.y += gravity * delta 
	if is_on_wall():
		_velocity.x *= -1.0
	_velocity.y = move_and_slide(_velocity, FLOOR_NORMAL).y
	
func die() -> void:
	queue_free()
	PlayerData.score += score


