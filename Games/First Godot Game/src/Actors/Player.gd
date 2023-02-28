extends Actor

onready var anim_player: AnimationPlayer = $AnimationPlayer

export var stomp_impulse = 1000.0

func _on_EnemyDetector_body_entered(body):
	die()

func _on_EnemyDetector_area_entered(area):
	#if area.global_position.y > get_node("player").global_position.y:
	#	return
	_velocity = calculate_stomp_velocity(_velocity, stomp_impulse)

func _physics_process(delta: float) -> void:
	var is_jump_interrupted: = Input.is_action_just_released("jump") and _velocity.y < 0.0
	var direction = get_direction()
	_velocity = calculate_move_velocity(_velocity,direction,speed, is_jump_interrupted)
	if Input.is_action_just_pressed("jump") and is_on_floor():
		anim_player.play("jump")
	_velocity = move_and_slide(_velocity, FLOOR_NORMAL)

func get_direction() -> Vector2:
	return Vector2(
		Input.get_action_strength("move_right")-Input.get_action_strength("move_left"),
		-Input.get_action_strength("jump") if is_on_floor() and Input.is_action_just_pressed("jump") else 0.0
	)
	
func landing() -> void:
	anim_player.play("land")

func calculate_move_velocity(linear_velocity: Vector2,
direction: Vector2,
speed: Vector2,
is_jump_interrupted: bool
) -> Vector2:
	var new_velocity: = linear_velocity
	new_velocity.x = speed.x * direction.x
	new_velocity.y += gravity * get_physics_process_delta_time()
	if direction.y == -1.0:
		new_velocity.y = speed.y * direction.y
	if is_jump_interrupted:
		new_velocity.y = 0.0
	return new_velocity

func calculate_stomp_velocity(linear_velocity: Vector2, impulse: float) -> Vector2:
	var out: = linear_velocity
	out.y = -impulse
	return out

func die() -> void:
	PlayerData.deaths += 1
	queue_free()


