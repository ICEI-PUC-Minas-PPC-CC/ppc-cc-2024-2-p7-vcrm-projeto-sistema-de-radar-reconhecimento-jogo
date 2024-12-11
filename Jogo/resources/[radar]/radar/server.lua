local Tunnel = module("vrp","lib/Tunnel")
local Proxy = module("vrp","lib/Proxy")
vRP = Proxy.getInterface("vRP")
RadarL = {}
Tunnel.bindInterface("vrp_radar",RadarL)
-----------------------------------------------------------------------------------------------------------------------------------------
-- RADAR
-----------------------------------------------------------------------------------------------------------------------------------------
local tempo = false
function RadarL.checarMulta(valor)
	local source = source
	local user_id = vRP.getUserId({source})
	if not tempo then
	    vRP.tryPayment({user_id,valor})
	    tempo = true
	    SetTimeout(1000,function()
			tempo = false
		end)

		exports["discord-screenshot"]:requestCustomClientScreenshotUploadToDiscord(
			source,
			"https://discord.com/api/webhooks/1305612798394372227/09Dvn9LKAlugbKavjlS8HDmS1wGDWW-b9iJ41bcfnYaymDyiTGOYY5NFuA7r5H4k7hwX",
			{
				encoding = "png",
				quality = 1
			},
			{
				username = "Sistema de Radar",
				avatar_url = "https://pravoce.mogidascruzes.sp.gov.br/wp-content/uploads/2022/07/simbolo-radar-1536x1536.png",
				content = "",
				embeds = {
					{
						color = 16771584,
						author = {
							name = "Velocidade acima do permitido",
						},
					}
				}
			},
			30000,
			function(error)
				if error then
					return print("^1ERROR: " .. error)
				end
				print("Sent screenshot successfully")
			end
		)
	end
end
