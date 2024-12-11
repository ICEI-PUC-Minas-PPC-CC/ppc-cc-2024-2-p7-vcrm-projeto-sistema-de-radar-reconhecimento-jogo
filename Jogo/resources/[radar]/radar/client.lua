vRP = Proxy.getInterface("vRP")
RadarL = Tunnel.getInterface("vrp_radar","vrp_radar")
-----------------------------------------------------------------------------------------------------------------------------------------
-- RADAR
-----------------------------------------------------------------------------------------------------------------------------------------
local radares = {
	{ ['x'] = 157.06420898438, ['y'] = -1028.8951416016, ['z'] = 29.320116043091 },
}

local tempo = false
local tempo2 = false
Citizen.CreateThread(function()
	while true do
		Citizen.Wait(1)
		for _,v in pairs(radares) do
		    local ped = PlayerPedId()
		    local vehicle = GetVehiclePedIsIn(ped)
		    local distance = GetDistanceBetweenCoords(v.x,v.y,v.z,GetEntityCoords(ped),true)
		    local speed = GetEntitySpeed(vehicle)*3.605936
		    if distance <= 8.0 then	
		        if IsEntityAVehicle(vehicle) then
			        if GetPedInVehicleSeat(vehicle,-1) then
				        if speed >= 101 and not tempo then
					        vRP.setDiv({"radar",".div_radar { background: #fff; margin: 0; width: 100%; height: 100%; opacity: 0.9; }",""})
					        PlaySoundFrontend( -1, "ATM_WINDOW", "HUD_FRONTEND_DEFAULT_SOUNDSET", 1 )
		                    SetTimeout(200,function()
			                    vRP.removeDiv({"radar"})
			                    tempo = true
		                    end)
		                    SetTimeout(1150,function()
					        	tempo = false
					        end)
				        end
				        if speed >= 60 and speed < 100  then
				        	RadarL.checarMulta({10})
				        	if not tempo2 then
				        		TriggerEvent('chatMessage',"ALERTA",{255,70,50},"Radar: Limite de velocidade permitido é 100KM/H, voce estava a "..math.ceil(speed).."KM/H, recebeu uma multa de $10!")
				        		tempo2 = true
				        		SetTimeout(1000,function()
					        	    tempo2 = false
					            end)
					        end
				        elseif speed >= 101 and speed < 200  then
				        	RadarL.checarMulta({20})
				        	if not tempo2 then
				        		TriggerEvent('chatMessage',"ALERTA",{255,70,50},"Radar: Limite de velocidade permitido é 100KM/H, voce estava a "..math.ceil(speed).."KM/H, recebeu uma multa de $20!")
				        		tempo2 = true
				        		SetTimeout(1000,function()
					        	    tempo2 = false
					            end)
					        end
				        elseif speed >= 201 and speed < 250  then
                            RadarL.checarMulta({30})
                            if not tempo2 then
				        		TriggerEvent('chatMessage',"ALERTA",{255,70,50},"Radar: Limite de velocidade permitido é 100KM/H, voce estava a "..math.ceil(speed).."KM/H, recebeu uma multa de $30!")
				        		tempo2 = true
				        		SetTimeout(1000,function()
					        	    tempo2 = false
					            end)
					        end
                        elseif speed >= 251  then
                        	RadarL.checarMulta({40})
                        	if not tempo2 then
				        		TriggerEvent('chatMessage',"ALERTA",{255,70,50},"Radar: Limite de velocidade permitido é 100KM/H, voce estava a "..math.ceil(speed).."KM/H, recebeu uma multa de $40!")
				        		tempo2 = true
				        		SetTimeout(1000,function()
					        	    tempo2 = false
					            end)
					        end
                        end
				    end
				end
			end
		end
	end
end)