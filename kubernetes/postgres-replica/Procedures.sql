CREATE OR REPLACE FUNCTION pub.findCodGrupsByIdUsuarios(idUsuarios text[])
RETURNS SETOF text AS $$

    SELECT grp.cod_grp FROM pub.rwm_grp grp
            INNER JOIN pub.rwm_grp_usr grp_usr ON grp.cod_grp = grp_usr.cod_grp
            INNER JOIN pub.rwm_usuario usr ON usr.id_usuario = grp_usr.id_usuario 
            where usr.id_usuario = ANY(idUsuarios) AND grp.ativo = true AND grp.tipo = 'padrao'

$$
LANGUAGE SQL;


CREATE OR REPLACE FUNCTION pub.findUsersByCirculosAndIdUsuario(codCirculos text[], idUsuarios text[])
RETURNS TABLE(
id_usuario text
) AS $$
	
    SELECT * FROM pub.rwm_usuario u
            INNER JOIN pub.rwm_grp_usr grp_usr ON u.id_usuario = grp_usr.id_usuario
            INNER JOIN pub.rwm_grp grp ON grp.cod_grp = grp_usr.cod_grp
            INNER JOIN pub.rwm_grp_rel grp_rel ON grp.cod_grp = grp_rel.cod_grp
            INNER JOIN pub.rwm_circulo circulo ON grp_rel.cod_circulo = circulo.cod_circulo
            where grp_rel.cod_circulo = ANY(codCirculos) AND grp.cod_grp = ANY(pub.findCodGrupsByIdUsuarios(idUsuarios)) AND grp.ativo = true AND circulo.ativo = true

$$
LANGUAGE SQL;

