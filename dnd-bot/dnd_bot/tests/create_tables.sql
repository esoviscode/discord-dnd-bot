CREATE TABLE public."Game"
(
    id_game BIGSERIAL NOT NULL,
    token VARCHAR,
    id_host BIGINT,
    game_state VARCHAR,
	campaign_name VARCHAR,
    PRIMARY KEY (id_game),
    CONSTRAINT game_state_enum CHECK (game_state in ('LOBBY', 'STARTING', 'ACTIVE', 'INACTIVE', 'FINISHED'))
);

ALTER TABLE IF EXISTS public."Game"
    OWNER to admin;
	

CREATE TABLE public."User"
(
    id_user BIGSERIAL NOT NULL,
    id_game BIGINT,
    discord_id BIGINT,
    PRIMARY KEY (id_user),
    CONSTRAINT id_game FOREIGN KEY (id_game)
        REFERENCES public."Game" (id_game) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."User"
    OWNER to admin;


CREATE TABLE public."Event"
(
    id_event BIGSERIAL NOT NULL,
    x INTEGER,
    y INTEGER,
    range INTEGER,
    status VARCHAR,
    content VARCHAR,
    id_game BIGINT,
    PRIMARY KEY (id_event),
    CONSTRAINT id_game FOREIGN KEY (id_game)
        REFERENCES public."Game" (id_game) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT status_enum CHECK (status in ('AVAILABLE', 'NOT_AVAILABLE'))
);

ALTER TABLE IF EXISTS public."Event"
    OWNER to admin;
	
	
CREATE TABLE public."Entity"
(
    id_entity BIGSERIAL NOT NULL,
    name VARCHAR,
    x INTEGER,
    y INTEGER,
    sprite VARCHAR,
    id_game BIGINT,
    PRIMARY KEY (id_entity),
    CONSTRAINT id_game FOREIGN KEY (id_game)
        REFERENCES public."Game" (id_game) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Entity"
    OWNER to admin;
	

CREATE TABLE public."Creature"
(
    id_creature BIGSERIAL NOT NULL,
    level INTEGER,
    "HP" INTEGER,
    strength INTEGER,
    dexterity INTEGER,
    intelligence INTEGER,
    charisma INTEGER,
    perception INTEGER,
    initiative INTEGER,
    action_points INTEGER,
    money INTEGER,
    id_entity BIGINT,
    PRIMARY KEY (id_creature),
    CONSTRAINT base_entity FOREIGN KEY (id_entity)
        REFERENCES public."Entity" (id_entity) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Creature"
    OWNER to admin;
	
	
CREATE TABLE public."Dialog"
(
    id_dialog BIGSERIAL NOT NULL,
    id_speaker BIGINT,
    id_listener BIGINT,
    content VARCHAR,
    status VARCHAR,
    PRIMARY KEY (id_dialog),
    CONSTRAINT id_speaker FOREIGN KEY (id_speaker)
        REFERENCES public."Entity" (id_entity) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT id_listener FOREIGN KEY (id_listener)
        REFERENCES public."Entity" (id_entity) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT status_enum CHECK (status in ('AVAILABLE', 'NOT_AVAILABLE', 'USED'))
);

ALTER TABLE IF EXISTS public."Dialog"
    OWNER to admin;
	
	
CREATE TABLE public."Item"
(
    id_item BIGSERIAL NOT NULL,
    name VARCHAR,
    "HP" INTEGER,
    strength INTEGER,
    dexterity INTEGER,
    intelligence INTEGER,
    charisma INTEGER,
    perception INTEGER,
    action_points INTEGER,
    effect VARCHAR,
    base_price INTEGER,
    PRIMARY KEY (id_item)
);

ALTER TABLE IF EXISTS public."Item"
    OWNER to admin;
	
	
CREATE TABLE public."Creature_Item"
(
    id_creature_item BIGSERIAL NOT NULL,
    id_creature BIGINT,
    id_item BIGINT,
    amount INTEGER,
    PRIMARY KEY (id_creature_item),
    CONSTRAINT id_creature FOREIGN KEY (id_creature)
        REFERENCES public."Creature" (id_creature) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT id_item FOREIGN KEY (id_item)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Creature_Item"
    OWNER to admin;
	
	
CREATE TABLE public."Skill"
(
    id_skill BIGSERIAL NOT NULL,
    name VARCHAR,
    PRIMARY KEY (id_skill)
);

ALTER TABLE IF EXISTS public."Skill"
    OWNER to admin;	
	
	
CREATE TABLE public."Entity_Skill"
(
    id_entity_skill BIGSERIAL NOT NULL,
    id_entity BIGINT,
    id_skill BIGINT,
    PRIMARY KEY (id_entity_skill),
    CONSTRAINT id_entity FOREIGN KEY (id_entity)
        REFERENCES public."Entity" (id_entity) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT id_skill FOREIGN KEY (id_skill)
        REFERENCES public."Skill" (id_skill) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Entity_Skill"
    OWNER to admin;
	
CREATE TABLE public."Equipment"
(
    id_equipment BIGSERIAL NOT NULL,
    helmet BIGINT,
    chest BIGINT,
    leg_armor BIGINT,
    boots BIGINT,
    left_hand BIGINT,
    right_hand BIGINT,
    accessory BIGINT,
    PRIMARY KEY (id_equipment),
    CONSTRAINT helmet FOREIGN KEY (helmet)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT chest FOREIGN KEY (chest)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT leg_armor FOREIGN KEY (leg_armor)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT boots FOREIGN KEY (boots)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT left_hand FOREIGN KEY (left_hand)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT right_hand FOREIGN KEY (right_hand)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT accessory FOREIGN KEY (accessory)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL
);

ALTER TABLE IF EXISTS public."Equipment"
    OWNER to admin;
	
	
CREATE TABLE public."Player"
(
    id_player BIGSERIAL NOT NULL,
    id_user BIGINT,
    alignment VARCHAR,
    backstory VARCHAR,
    id_equipment BIGINT,
    id_creature BIGINT,
    PRIMARY KEY (id_player),
    CONSTRAINT id_user FOREIGN KEY (id_user)
        REFERENCES public."User" (id_user) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT id_equipment FOREIGN KEY (id_equipment)
        REFERENCES public."Equipment" (id_equipment) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT id_creature FOREIGN KEY (id_creature)
        REFERENCES public."Creature" (id_creature) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Player"
    OWNER to admin;
    