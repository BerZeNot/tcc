from lib.get_zeros import get_zeros

def get_mountains(vector,buf):
    # divide a função em vários pedaços, "montanhas"
    # isto é, de zero até uma valor máximo (ou mínimo) e de volta ao zero
    # ERRO:
    # o vetor deve ter tamanho 255 e as primeiras pontas são zeradas!
    # o erro está muito baixo
    #
    # normalizei o vetor de comparacão para considerar como zeros valores
    # 1e-5. Ver se esse é o método correto
    #
    #

    #vecd = fftderiv(vector,n=1,sigma=3);
    vecd = (vector)/(max(vector(:))-min(vector(:)));

    #encontrando os pontos que são zeros

    vecd(1:buf) = 0;
    vecd(end-buf:end) = 0;

    zer = get_zeros(vecd,1e-4);

    p1 = zer(1:end-1,2);
    p2 = zer(2:end,1);

    mon = zeros(size(vecd));
    mon_max = [];
    mon_max_pos = [];

    # montanhas iniciais
    for ip=1:numel(p1)
    val = vector(p1(ip):p2(ip));
    [mmax, mmaxpos] = max(abs(val(:)));
    mon_max(ip) = mmax;
    mon_max_pos(ip) = p1(ip) + mmaxpos -1;
    end
    [mon_max,k] = sort(mon_max,'descend');
    mon_max_pos = mon_max_pos(k);

    # montanhas ordenadas
    for ip=1:numel(p1)
    mon(p1(k(ip)):p2(k(ip)))= ip;
    end