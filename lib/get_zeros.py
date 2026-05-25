def get_zeros(vet,delta):

  pos = find(vet>=-delta & vet <=delta)

  # procurando por mudança no sinal
  # é bom colocar +1 no zero cross pois garante que o ponto 
  # vai estar do outro lado  do eixo
  zerocross = find(xor(vet(1:end-1)>delta,vet(2:end)>delta))+1
  pos = [pos  zerocross ]
  pos = sort(pos)

  if ~isempty(pos)
    dif =  pos(2:end)-pos(1:end-1) 
    inicio = [pos(1)  pos(find(dif>1)+1)]
    fim = [pos(find(dif>1)) pos(end)]
    tam = fim-inicio+1
    zer = [ inicio' fim' tam']
  else
    zer = []
  end  