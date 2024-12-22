delimiter // 
DROP TRIGGER IF EXISTS `atualiza_listaDeFerramentas` //
Create trigger atualiza_listaDeFerramentas  
before insert on registroDeSaidasDeEquips 
for each row 
begin  

if  (select count(*) from listaDeFerramentas where tipoENumero = new.Ferramenta) = 0 then  
insert into listaDeFerramentas (TipoENumero) values (new.Ferramenta);
end if; 

update listaDeFerramentas set responsavelAtual = new.Funcionario, idUltimoRegistro=new.id where listaDeFerramentas.tipoENumero = new.Ferramenta; 

end//
delimiter ;

delimiter // 
DROP TRIGGER IF EXISTS `atualiza_volta_listaDeFerramentas` //
Create trigger atualiza_volta_listaDeFerramentas  
after update on registroDeSaidasDeEquips 
for each row 
begin 

if  (select count(*) from listaDeFerramentas where tipoENumero = new.Ferramenta) = 0 then  
insert into listaDeFerramentas (TipoENumero) values (new.Ferramenta);
end if; 

update listaDeFerramentas set responsavelAtual = 'almoxarifado' where listaDeFerramentas.tipoENumero = new.Ferramenta; 

end //
delimiter ;



delimiter //
DROP TRIGGER IF EXISTS `VoltaNaoRegistrada` // 
Create trigger VoltaNaoRegistrada 
before insert on registroDeSaidasDeEquips 
for each row 
begin 

if  (select count(*) from registroDeSaidasDeEquips where Ferramenta = new.Ferramenta and DataRetorno is null)  <> 0 then  

update registroDeSaidasDeEquips set DataRetorno = current_date(),HorarioRetorno = current_time()   
where Ferramenta = New.Ferramenta and DataRetorno is null;

end if; 

update listaDeFerramentas set responsavelAtual = new.Funcionario where listaDeFerramentas.tipoENumero = new.Ferramenta; 

end //
delimiter ;
