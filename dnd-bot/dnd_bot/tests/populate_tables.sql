INSERT INTO public."Game"(
	token, id_host, game_state, campaign_name)
	VALUES ('12345', 678, 'LOBBY', 'test_campaign');

INSERT INTO public."User"(id_game, discord_id) VALUES (1, 111);
INSERT INTO public."User"(id_game, discord_id) VALUES (1, 222);
INSERT INTO public."User"(id_game, discord_id) VALUES (1, 222);

