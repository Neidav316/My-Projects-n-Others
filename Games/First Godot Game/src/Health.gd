extends Node

const MAX_HEALTH : = 100
var health :  = MAX_HEALTH

func take_damage(amount:int) -> void:
	health -= amount
	health = max(0,health)

func get_health(amount:int) -> void: 
	health += amount
	health = min(health, MAX_HEALTH)
