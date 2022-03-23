CREATE TABLE pub.rwm_usuario (
  id_usuario varchar (12) PRIMARY KEY,
  perfil integer null,
  cod_usuario varchar (12) null,
  ativo boolean null,
  dt_val_ini date null,
  dt_val_fim date null,
  senha varchar (40) null,
  dt_cadastro date null,
  email varchar (300) null,
  qt_login_seg integer null,
  senha_bloqueada boolean null,
  nivel integer null,
  dt_ult_acesso date null,
  dt_ult_login date null,
  num_dias_val_senha integer null,
  dt_valida_senha date null,
  cod_grp integer null,
  cod_usuario_ems varchar (12) null,
  nome varchar (60) null,
  tp_hierarquia integer null,
  telefone varchar (20) null,
  lista_rep_ind varchar (300) null,
  celular varchar (20) null,
  lista_rep_ind_nom varchar (300) null,
  id_super varchar (12) null,
  lista_cli_ind varchar (300) null,
  lista_cli_ind_nom varchar (300) null,
  lista_uf_acesso varchar (100) null,
  ind_hier_atual boolean null,
  lib_man_pedido boolean null,
  lib_man_cliente boolean null,
  lib_man_pedido_sub boolean null,
  lib_man_cliente_sub boolean null,
  lista_grp varchar (1000) null,
  lista_papel varchar (1000) null
);

CREATE TABLE pub.rwm_grp (
  cod_grp varchar (40) PRIMARY KEY,
  descricao varchar (60) null,
  ativo boolean null,
  cod_label varchar (30) null,
  cod_cor varchar (30) null,
  tipo varchar (30) null,
  cod_obj_perm varchar (40) null,
  prioridade integer null
);

CREATE TABLE pub.rwm_circulo (
  cod_circulo varchar (40) null PRIMARY KEY,
  descricao varchar (60) null,
  ativo boolean null,
  cod_obj_perm varchar (40) null,
  tp_relation varchar (40) null,
  cod_obj_prop_rel varchar (40) null
);

CREATE TABLE pub.rwm_grp_usr (
  cod_grp varchar (30) null,
  id_usuario varchar (12) null,
  PRIMARY KEY (cod_grp, id_usuario)
);

CREATE TABLE pub.rwm_grp_rel (
  cod_circulo varchar (40) null,
  cod_grp varchar (40) null,
  cod_grp_rel varchar (40) null,
  ativo boolean null,
  tp_rel varchar (200) null,
  PRIMARY KEY (cod_circulo, cod_grp, cod_grp_rel)
);

CREATE TABLE pub.rwm_circulo_grp (
  cod_circulo varchar (40) null,
  cod_grp varchar (40) null,
  cod_pai varchar (40) null,
  seq integer null,
  seq_pai integer null,
  PRIMARY KEY (cod_circulo, cod_grp, cod_pai, seq, seq_pai)
);

CREATE TABLE pub.rwm_usuario_rel (
  cod_circulo varchar (40) null,
  id_usuario varchar (12) null,
  id_usuario_rel varchar (12) null,
  PRIMARY KEY (cod_circulo, id_usuario, id_usuario_rel)
);

CREATE TABLE pub.rwm_objeto_perm (
  cod_container varchar (40) null,
  cod_obj varchar (40) null,
  cod_grp varchar (40) null,
  id_usuario varchar (12) null,
  cod_container_ref varchar (40) null,
  cod_obj_ref varchar (40) null,
  tp_behavior varchar (40) null,
  tp_permission varchar (40) null,
  cod_objeto_lista varchar (40) null,
  valor text null,
  PRIMARY KEY (cod_obj,cod_grp,cod_container,id_usuario,cod_container_ref,cod_obj_ref)
);

CREATE TABLE pub.rwm_objeto (
  cod_container varchar (40) null,
  cod_obj varchar (40) null,
  cod_grp varchar (40) null,
  id_usuario varchar (12) null,
  cod_container_ref varchar (40) null,
  cod_obj_ref varchar (40) null,
  tp_behavior varchar (40) null,
  tipo_var varchar (20) null,
  val_date date null,
  val_decimal decimal(11,2) null,
  val_decimal3 decimal(12,3) null,
  val_decimal4 decimal(13,4) null,
  val_decimal5 decimal(14,5) null,
  val_decimal6 decimal(15,6) null,
  val_integer integer null,
  val_logical boolean null,
  desc_label varchar (100) null,
  cod_grp_config varchar (40) null,
  cod_objeto_lista varchar (40) null,
  perfil integer null,
  cod_usuario varchar (12) null,
  tab_docto varchar (100) null,
  tp_objeto varchar (40) null,
  nome_arq text null,
  is_large boolean null,
  cod_obj_config varchar (40) null,
  extensao varchar (40) null,
  cod_categ varchar (40) null,
  permissao varchar (100) null,
  dir_root varchar (40) null,
  cod_obj_perm varchar (40) null,
  list_obj_replace varchar (500) null,
  save_content boolean null,
  col_label varchar (40) null,
  file_wm boolean null,
  valor text null,
  descricao text null,
  tp_usuario varchar (15) null,
  ativo boolean null,
  dt_last_update date null,
  dt_last_update_val date null,
  config_replace text null,
  list_prop varchar (1000) null,
  PRIMARY KEY (cod_obj,cod_grp,cod_container,id_usuario,cod_container_ref,cod_obj_ref)
);


