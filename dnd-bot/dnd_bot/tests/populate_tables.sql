INSERT INTO public."Game"(
	token, id_host, game_state, campaign_name, active_creature)
	VALUES ('12345', 678, 'LOBBY', 'test_campaign', 123);
INSERT INTO public."Game"(
	token, id_host, game_state, campaign_name, active_creature)
	VALUES ('67890', 323, 'ACTIVE', 'test_campaign2', 123);

INSERT INTO public."User"(id_game, discord_id) VALUES (1, 111);
INSERT INTO public."User"(id_game, discord_id) VALUES (1, 222);
INSERT INTO public."User"(id_game, discord_id) VALUES (1, 222);

