Relatório de Alterações
Comparando o código mais antigo com o código antigo, identifiquei as seguintes mudanças realizadas:

1. Troca do OCR
Anterior: Usava o Tesseract (pytesseract).
Alterado: Passou a usar o PaddleOCR.
Substituição da função scan_plate por scan_plate_with_paddleocr para trabalhar com o PaddleOCR.

2. Pré-Processamento
Anterior: Usava funções como thresholding (técnica de processamento de imagem que converte uma imagem em preto e branco com base em um valor limite: pixels acima do limite ficam brancos, e os abaixo ficam pretos) da biblioteca local.
Alterado: Foi introduzida a aplicação de Threshold OTSU (Ele usa análise estatística para maximizar a separação entre os dois grupos de pixels (objetos e fundo), sem a necessidade de definir o limite manualmente) diretamente no código.

3. Redimensionamento de Imagens
Novo: Foi adicionada a função resize_image para ajustar o tamanho das imagens e melhorar a leitura do OCR

4. Correção de Caracteres
Novo: Implementação de uma função para corrigir caracteres reconhecidos erroneamente.

5. Logs e Depuração
Novo: Adição de funções de log para depuração e salvamento de etapas intermediárias.

6. Formatação e Salvamento de Resultados
Novo: Implementação de salvamento dos resultados em um arquivo CSV.

7. Processamento de Arquivos
Anterior: As imagens eram processadas de uma lista fixa.
Alterado: Agora as imagens são carregadas dinamicamente de um diretório.

8. Estrutura Principal
Anterior: Usava um fluxo simples e chamava main() diretamente.
Alterado: Foi reformulado para incluir funções mais detalhadas e para ser executado como script principal.