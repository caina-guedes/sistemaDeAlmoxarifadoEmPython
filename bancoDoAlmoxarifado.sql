CREATE TABLE `funcionarios`(
    `nome` VARCHAR(64) NOT NULL,
    `funcao` VARCHAR(64) NULL,
    `nomeCompleto` VARCHAR(511) NULL,
    `EquipsDeCampo` SMALLINT NULL DEFAULT '0' COMMENT 'quantidade de equipamentos com o funcionario em campo para uso diário',
    `equipsForaDaObra` SMALLINT NULL DEFAULT '0' COMMENT 'quantidade de ferramentas/equipamentos levados para fora da obra por esse funcionario',
    `idObs` BIGINT NULL
);
CREATE TABLE `siglasENomesDeEquips`(
    `abreviaturaDeEquipamento` VARCHAR(64) NOT NULL,
    `nomeCompleto` VARCHAR(64) NOT NULL,
    `possuiNumeracao` BOOLEAN NULL,
    `alcanceDaNumeracao` INT NULL,
    `idObs` BIGINT NULL
);
CREATE TABLE `registroDeSaidasDeEquips`(
    `Ferramenta` VARCHAR(64) NOT NULL,
    `Funcionario` VARCHAR(64) NOT NULL,
    `DataSaida` DATE NULL,
    `HorarioSaida` TIME NULL COMMENT 'quando estiver com valor nulo significa que o equipamento não voltou',
    `DataRetorno` DATE NULL COMMENT 'essa coluna é para diferenciar quem levou para uso em campo de quem levou para fora do campo',
    `HorarioRetorno` TIME NULL,
    `usoExterno` BOOLEAN NOT NULL DEFAULT '0' COMMENT 'verdadeiro se a ferramenta tiver sido levada para fora da obra',
    `devolvedor` VARCHAR(64) NULL,
    `idObs` BIGINT NULL,
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `identificador` VARCHAR(32) NULL COMMENT 'essa coluna vai armazenar a identificação unica da ferramenta',
    `revisada` BOOLEAN NOT NULL DEFAULT '0'
);
CREATE TABLE `listaDeFerramentas`(
    `tipoENumero` VARCHAR(64) NOT NULL COMMENT 'ferramenta seguida de sua numeracao',
    `responsavelAtual` VARCHAR(64) NOT NULL DEFAULT 'almoxarifado' COMMENT 'se estiver fora, conterá o nome de quem pegou',
    `dentroDaObra` BOOLEAN NULL DEFAULT '1' COMMENT 'verdadeiro se o equipamento não saiu da obra',
    `estadoNumeracao` VARCHAR(64) NULL,
    `idObs` BIGINT NULL,
    `quantidade` BIGINT NULL,
    `idUltimoRegistro` BIGINT NULL
);
CREATE TABLE `consumíveisDaObra`(
    `consumível` VARCHAR(128) NOT NULL,
    `checagemDiaria` BOOLEAN NULL,
    `checagemSemanal` BOOLEAN NULL,
    `quantidade` INT NULL,
    `checagemEmDia` BOOLEAN NULL,
    `ultimaChecagem` DATE NULL,
    `idObs` BIGINT NULL COMMENT 'coluna utilizada para manter a rotina de controle de consumíveis em dia'
);
CREATE TABLE `observacoes`(
    `Observacao` VARCHAR(1024) NOT NULL,
    `funcionario` VARCHAR(64) NULL,
    `ferramenta` VARCHAR(64) NULL,
    `consumível` VARCHAR(64) NULL,
    `tabela` VARCHAR(64) NULL COMMENT 'origem dessa observacao em relação as outras tabelas.',
    `key` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY
);
CREATE TABLE `manutencaoExterna`(
    `ferramenta` VARCHAR(64) NOT NULL,
    `Saida` DATE NULL,
    `Retorno` DATE NULL,
    `problema` VARCHAR(1024) NULL,
    `responsavelPelaManutencao` VARCHAR(64) NULL,
    `resultado` VARCHAR(64) NULL,
    `idObs` BIGINT NULL
);
CREATE TABLE `manutençãoInterna`(
    `ferramenta` VARCHAR(64) NOT NULL,
    `DescricaoDoProblema` VARCHAR(1024) NOT NULL,
    `resolvido` BOOLEAN NOT NULL DEFAULT '0',
    `idObs` BIGINT NULL
);
CREATE TABLE `inventarioDeEquipamentosEFerramentas`(
    `ferramenta` VARCHAR(127) NOT NULL,
    `quantidade` BIGINT NOT NULL,
    `data` DATE NOT NULL,
    `estado` VARCHAR(64) NULL,
    `obsDaFerramenta` VARCHAR(1023) NULL,
    `marca` VARCHAR(64) NULL,
    `modelo` VARCHAR(64) NULL,
    `categoria` VARCHAR(64) NULL COMMENT 'essa coluna servirá para separar as coisas de acordo com a necessidade, por exemplo equipamentos eletricos, ferramentas manuais ou a combustível, etc'
);
CREATE TABLE `discrepanciasDeEquipamentos`(
    `ferramenta` VARCHAR(64) NULL,
    `funcionario` VARCHAR(64) NULL,
    `discrepancia` VARCHAR(1028) NULL
);
CREATE TABLE `variaveisQuePersistem`(
    `funcionarioAtual` VARCHAR(128) NULL,
    `modoAtual` VARCHAR(128) NULL,
    `dataUltimoCommit` DATE NULL,
    `horaUltimoCommit` TIME NULL
);