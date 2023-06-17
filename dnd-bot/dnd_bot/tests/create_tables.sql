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
    discord_channel BIGINT,
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
    status VARCHAR,
    id_game BIGINT,
    json_id BIGINT,
    PRIMARY KEY (id_event),
    CONSTRAINT id_game FOREIGN KEY (id_game)
        REFERENCES public."Game" (id_game) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT status_enum CHECK (status in ('AVAILABLE', 'NOT_AVAILABLE'))
);

ALTER TABLE IF EXISTS public."Event"
    OWNER to admin;


CREATE TABLE public."Item"
(
    id_item BIGSERIAL NOT NULL,
    name VARCHAR,
    PRIMARY KEY (id_item)
);

ALTER TABLE IF EXISTS public."Item"
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


CREATE TABLE public."Entity"
(
    id_entity BIGSERIAL NOT NULL,
    name VARCHAR,
    x INTEGER,
    y INTEGER,
    id_game BIGINT,
    description VARCHAR,
    look_direction VARCHAR,
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
    id_entity BIGINT NOT NULL,
    experience INTEGER,
    id_equipment BIGINT,
    class VARCHAR,
    max_hp INTEGER,
    initial_action_points INTEGER,
    PRIMARY KEY (id_creature),
    CONSTRAINT base_entity FOREIGN KEY (id_entity)
        REFERENCES public."Entity" (id_entity) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT id_equipment FOREIGN KEY (id_equipment)
        REFERENCES public."Equipment" (id_equipment) MATCH SIMPLE
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT class_enum CHECK (class in ('WARRIOR', 'MAGE', 'RANGER'))
);

ALTER TABLE IF EXISTS public."Creature"
    OWNER to admin;


CREATE TABLE public."Player"
(
    id_player BIGSERIAL NOT NULL,
    id_user BIGINT,
    alignment VARCHAR,
    backstory VARCHAR,
    id_creature BIGINT NOT NULL,
    race VARCHAR,
    PRIMARY KEY (id_player),
    CONSTRAINT id_user FOREIGN KEY (id_user)
        REFERENCES public."User" (id_user) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT id_creature FOREIGN KEY (id_creature)
        REFERENCES public."Creature" (id_creature) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT race_enum CHECK (race in ('HUMAN', 'ELF', 'DWARF'))
);

ALTER TABLE IF EXISTS public."Player"
    OWNER to admin;


CREATE TABLE public."Dialog"
(
    id_dialog BIGSERIAL NOT NULL,
    id_speaker BIGINT,
    id_listener BIGINT,
    content VARCHAR,
    status VARCHAR,
    json_id BIGINT,
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


CREATE TABLE public."Player_Item"
(
    id_player BIGINT NOT NULL,
    id_item BIGINT NOT NULL,
    amount INTEGER,
    PRIMARY KEY (id_player, id_item),
    CONSTRAINT id_player FOREIGN KEY (id_player)
        REFERENCES public."Player" (id_player) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT id_item FOREIGN KEY (id_item)
        REFERENCES public."Item" (id_item) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public."Player_Item"
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
    id_entity BIGINT NOT NULL,
    id_skill BIGINT NOT NULL,
    PRIMARY KEY (id_entity, id_skill),
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

ALTER TABLE public."Game"
ADD COLUMN active_creature BIGINT;

ALTER TABLE public."Game"
ADD CONSTRAINT active_creature FOREIGN KEY (active_creature)
REFERENCES public."Creature" (id_creature) MATCH SIMPLE
        ON UPDATE CASCADE;