extends Node


var character_name :  = "Jaimy"
const MAX_HEALTH : = 100
var health :  = MAX_HEALTH
var run_speed :  = 200.0
var map : TileMap
var body : Sprite


# Called when the node enters the scene tree for the first time.
func _ready():

	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.

func _process(delta):
	if health <= 0:
		_die()
	if health >= MAX_HEALTH:
		health = MAX_HEALTH
	pass
	
func _die():
	pass
