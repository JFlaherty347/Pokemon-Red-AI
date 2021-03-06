-- require 'pylist'

--main functions
function progress()
	final_reward = moneyReward()
	final_reward = final_reward + partyReward()
	final_reward = final_reward + pkmn1XPReward()
	final_reward = final_reward + overworldMovementReward()
	final_reward = final_reward + explorationReward()
	final_reward = final_reward + timePunishment()

	return final_reward
end

function done_check()
	-- finish once 2 pokemon are obtained
	if data.party_size == 1 then
		return true
	end
	return false
end

--reward functions
previous_money = 3000
previous_party_size = 0
previous_pkmn1_exp = 0

previous_xPos = 0
previous_yPos = 0
movement_counter = 0
movement_counter_limit = 90

visitedMaps = {}

function moneyReward()
	return (data.money - previous_money) * 0.0005
end

function partyReward()
	return (data.party_size - previous_party_size) * 1000
end

function pkmn1XPReward()
	return (data.totalExpPkmn1 - previous_pkmn1_exp) * 6
end

function overworldMovementReward()
	final_reward = 0
	if (data.xPosOverworld ~= previous_xPos or data.yPosOverworld ~= previous_yPos) then
		previous_xPos = data.xPosOverworld
		previous_yPos = data.yPosOverworld
		movement_counter = 0
	elseif movement_counter > movement_counter_limit then
		movement_counter = movement_counter + 1
		final_reward = -12
	else
		movement_counter = movement_counter + 1
	end

	return final_reward
end

function explorationReward()
	final_reward = 0
	if setContains(visitedMaps, data.mapID) then
		print("Exploring a new map!")
		addToSet(visitedMaps, data.mapID)
		final_reward = 100
	end

	return final_reward
end

function timePunishment()
	return -0.04
end

--list helper functions

function addToSet(set, key)
    set[key] = true
end

function removeFromSet(set, key)
    set[key] = nil
end

function setContains(set, key)
    return set[key] ~= nil
end
