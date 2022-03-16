CREATE TABLE pub."rwm_usuario" (
  "id_usuario" varchar (12) not null PRIMARY KEY,
  "perfil" integer null,
  "cod_usuario" varchar (12) not null,
  "ativo" boolean not null,
  "dt_val_ini" date null,
  "dt_val_fim" date null,
  "senha" varchar (40) null,
  "dt_cadastro" date null,
  "email" varchar (300) null,
  "qt_login_seg" integer null,
  "senha_bloqueada" boolean null,
  "nivel" integer null,
  "dt_ult_acesso" date null,
  "dt_ult_login" date null,
  "num_dias_val_senha" integer null,
  "dt_valida_senha" date null,
  "cod_grp" integer null,
  "cod_usuario_ems" varchar (12) null,
  "nome" varchar (60) null,
  "tp_hierarquia" integer null,
  "telefone" varchar (20) null,
  "lista_rep_ind" varchar (300) null,
  "celular" varchar (20) null,
  "lista_rep_ind_nom" varchar (300) null,
  "id_super" varchar (12) null,
  "lista_cli_ind" varchar (300) null,
  "lista_cli_ind_nom" varchar (300) null,
  "lista_uf_acesso" varchar (100) null,
  "ind_hier_atual" boolean null,
  "lib_man_pedido" boolean null,
  "lib_man_cliente" boolean null,
  "lib_man_pedido_sub" boolean null,
  "lib_man_cliente_sub" boolean null,
  "lista_grp" varchar (1000) null,
  "lista_papel" varchar (1000) null
);

CREATE TABLE pub."rwm_grp" (
  "cod_grp" varchar (40) not null PRIMARY KEY,
  "descricao" varchar (60) not null,
  "ativo" boolean null,
  "cod_label" varchar (30) null,
  "cod_cor" varchar (30) null,
  "tipo" varchar (30) null,
  "cod_obj_perm" varchar (40) null,
  "prioridade" integer null
);

CREATE TABLE pub."rwm_circulo" (
  "cod_circulo" varchar (40) not null PRIMARY KEY,
  "descricao" varchar (60) null,
  "ativo" boolean null,
  "cod_obj_perm" varchar (40) null,
  "tp_relation" varchar (40) null,
  "cod_obj_prop_rel" varchar (40) null
);

CREATE TABLE pub."rwm_grp_rel" (
  "cod_circulo" varchar (40) null,
  "cod_grp" varchar (40) null,
  "cod_grp_rel" varchar (40) null,
  "ativo" boolean null,
  "tp_rel" varchar (200) null
);

CREATE TABLE pub."rwm_circulo_grp" (
  "cod_circulo" varchar (40) null,
  "cod_grp" varchar (40) null,
  "cod_pai" varchar (40) null,
  "seq" integer null,
  "seq_pai" integer null
);