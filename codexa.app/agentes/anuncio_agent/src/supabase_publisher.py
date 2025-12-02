"""
Supabase Publisher - Integração para publicação autônoma de anúncios.

Este módulo permite ao anuncio_agent publicar produtos diretamente no site
GATO3 via Edge Functions do Supabase.

Requisitos:
- SUPABASE_URL: URL do projeto Supabase
- SUPABASE_SERVICE_ROLE_KEY: Chave service_role para autenticação admin

Uso:
    from supabase_publisher import SupabasePublisher

    publisher = SupabasePublisher()
    result = publisher.sync_product(product_id="uuid-do-produto")
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ============================================================================
# CONFIGURATION
# ============================================================================

SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "https://fuuguegkqnpzrrhwymgw.supabase.co"
)

SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

FUNCTIONS_BASE_URL = f"{SUPABASE_URL}/functions/v1"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class PublishResult:
    """Resultado de uma operação de publicação."""
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class ProductData:
    """Dados do produto para sincronização."""
    name: str
    description: str
    long_description: Optional[str] = None
    price: float = 0.0
    compare_at_price: Optional[float] = None
    quantity: int = 0
    images: Optional[list[str]] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    keywords: Optional[list[str]] = None
    bullet_points: Optional[list[str]] = None
    status: str = "draft"


# ============================================================================
# SUPABASE PUBLISHER
# ============================================================================

class SupabasePublisher:
    """
    Publisher para integração com Supabase Edge Functions.

    Permite operações administrativas:
    - sync_product: Sincroniza produto com Shopify
    - fetch_product: Busca dados atualizados do Shopify
    - create_product: Cria novo produto no Supabase
    """

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        service_role_key: Optional[str] = None
    ):
        """
        Inicializa o publisher.

        Args:
            supabase_url: URL do projeto Supabase (opcional, usa env var)
            service_role_key: Chave service_role (opcional, usa env var)
        """
        self.supabase_url = supabase_url or SUPABASE_URL
        self.service_role_key = service_role_key or SUPABASE_SERVICE_ROLE_KEY
        self.functions_url = f"{self.supabase_url}/functions/v1"

        if not self.service_role_key:
            print("[WARNING] SUPABASE_SERVICE_ROLE_KEY não configurada.")
            print("Configure via variável de ambiente ou passe no construtor.")

    def _make_request(
        self,
        endpoint: str,
        data: dict,
        method: str = "POST"
    ) -> tuple[bool, dict]:
        """
        Faz requisição autenticada para Edge Function.

        Args:
            endpoint: Nome da Edge Function
            data: Dados para enviar no body
            method: Método HTTP (default: POST)

        Returns:
            Tuple (success, response_data)
        """
        url = f"{self.functions_url}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": "application/json",
        }

        body = json.dumps(data).encode("utf-8")

        req = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(req, timeout=60) as response:
                response_body = response.read().decode("utf-8")
                return True, json.loads(response_body)

        except HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_data = json.loads(error_body)
            except json.JSONDecodeError:
                error_data = {"error": error_body}
            return False, {"error": error_data, "status_code": e.code}

        except URLError as e:
            return False, {"error": str(e.reason), "status_code": 0}

        except Exception as e:
            return False, {"error": str(e), "status_code": 0}

    def sync_product(self, product_id: str) -> PublishResult:
        """
        Sincroniza produto existente com Shopify.

        Cria ou atualiza o produto no Shopify baseado nos dados do Supabase.

        Args:
            product_id: UUID do produto no Supabase

        Returns:
            PublishResult com status da operação
        """
        if not self.service_role_key:
            return PublishResult(
                success=False,
                message="Service role key não configurada",
                error="SUPABASE_SERVICE_ROLE_KEY não definida"
            )

        success, response = self._make_request(
            "sync-shopify-product",
            {"productId": product_id}
        )

        if success:
            return PublishResult(
                success=True,
                message=response.get("message", "Produto sincronizado com sucesso"),
                data={
                    "shopify_product_id": response.get("shopifyProductId"),
                    "shopify_variant_id": response.get("shopifyVariantId"),
                }
            )
        else:
            return PublishResult(
                success=False,
                message="Falha ao sincronizar produto",
                error=str(response.get("error", "Erro desconhecido"))
            )

    def fetch_product(self, product_id: str) -> PublishResult:
        """
        Busca dados atualizados do produto no Shopify.

        Atualiza o Supabase com dados do Shopify (preço, estoque, etc).

        Args:
            product_id: UUID do produto no Supabase

        Returns:
            PublishResult com dados do produto
        """
        if not self.service_role_key:
            return PublishResult(
                success=False,
                message="Service role key não configurada",
                error="SUPABASE_SERVICE_ROLE_KEY não definida"
            )

        success, response = self._make_request(
            "fetch-from-shopify",
            {"productId": product_id}
        )

        if success:
            return PublishResult(
                success=True,
                message=response.get("message", "Dados buscados com sucesso"),
                data=response.get("data", {})
            )
        else:
            return PublishResult(
                success=False,
                message="Falha ao buscar dados do Shopify",
                error=str(response.get("error", "Erro desconhecido"))
            )

    def test_connection(self) -> PublishResult:
        """
        Testa conexão com o Supabase.

        Usa a função ronronalda-chat (pública) para verificar conectividade.

        Returns:
            PublishResult com status da conexão
        """
        # Testar função pública (não precisa de auth)
        try:
            url = f"{self.functions_url}/ronronalda-chat"
            headers = {"Content-Type": "application/json"}
            body = json.dumps({"message": "teste de conexão"}).encode("utf-8")

            req = Request(url, data=body, headers=headers, method="POST")

            with urlopen(req, timeout=30) as response:
                if response.status == 200:
                    return PublishResult(
                        success=True,
                        message="Conexão com Supabase OK",
                        data={"status_code": response.status}
                    )

        except Exception as e:
            return PublishResult(
                success=False,
                message="Falha na conexão com Supabase",
                error=str(e)
            )

        return PublishResult(
            success=False,
            message="Resposta inesperada do Supabase",
            error="Status code não esperado"
        )

    def test_admin_access(self) -> PublishResult:
        """
        Testa acesso admin com service_role key.

        Tenta fazer uma requisição às funções admin para verificar
        se a autenticação está funcionando.

        Returns:
            PublishResult com status do acesso admin
        """
        if not self.service_role_key:
            return PublishResult(
                success=False,
                message="Service role key não configurada",
                error="Configure SUPABASE_SERVICE_ROLE_KEY"
            )

        # Testar com um UUID inválido - esperamos erro de "produto não encontrado"
        # Se recebermos "não autorizado", a auth falhou
        success, response = self._make_request(
            "fetch-from-shopify",
            {"productId": "00000000-0000-0000-0000-000000000000"}
        )

        error_msg = str(response.get("error", ""))

        # Se o erro menciona "produto não encontrado", a auth funcionou
        if "não encontrado" in error_msg.lower() or "not found" in error_msg.lower():
            return PublishResult(
                success=True,
                message="Acesso admin OK - autenticação service_role funcionando",
                data={"auth": "ok"}
            )

        # Se o erro é de autorização, a auth falhou
        if "não autorizado" in error_msg.lower() or "unauthorized" in error_msg.lower():
            return PublishResult(
                success=False,
                message="Autenticação falhou",
                error="Service role key inválida ou expirada"
            )

        # Outro erro
        return PublishResult(
            success=False,
            message="Erro ao testar acesso admin",
            error=error_msg
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def publish_anuncio_to_supabase(
    product_id: str,
    service_role_key: Optional[str] = None
) -> PublishResult:
    """
    Função de conveniência para publicar anúncio.

    Args:
        product_id: UUID do produto no Supabase
        service_role_key: Chave service_role (opcional)

    Returns:
        PublishResult com status
    """
    publisher = SupabasePublisher(service_role_key=service_role_key)
    return publisher.sync_product(product_id)


def test_supabase_connection(
    service_role_key: Optional[str] = None
) -> dict[str, PublishResult]:
    """
    Testa conexão e acesso admin ao Supabase.

    Args:
        service_role_key: Chave service_role (opcional)

    Returns:
        Dict com resultados dos testes
    """
    publisher = SupabasePublisher(service_role_key=service_role_key)

    return {
        "connection": publisher.test_connection(),
        "admin_access": publisher.test_admin_access(),
    }


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("SUPABASE PUBLISHER - Teste de Conexão")
    print("=" * 60)

    # Verificar variáveis de ambiente
    print(f"\nSUPABASE_URL: {SUPABASE_URL}")
    print(f"SERVICE_ROLE_KEY: {'***' + SUPABASE_SERVICE_ROLE_KEY[-10:] if SUPABASE_SERVICE_ROLE_KEY else 'NÃO CONFIGURADA'}")

    # Executar testes
    print("\n--- Testando Conexão ---")
    results = test_supabase_connection()

    for test_name, result in results.items():
        status = "[OK]" if result.success else "[FAIL]"
        print(f"\n{status} {test_name}: {result.message}")
        if result.error:
            print(f"   Erro: {result.error}")
        if result.data:
            print(f"   Data: {result.data}")

    # Exemplo de uso
    print("\n--- Exemplo de Uso ---")
    print("""
# No seu código Python:

from supabase_publisher import SupabasePublisher

# Inicializar (usa env vars automaticamente)
publisher = SupabasePublisher()

# Ou passar keys diretamente
publisher = SupabasePublisher(
    service_role_key="eyJhbGciOiJIUzI1NiIs..."
)

# Sincronizar produto com Shopify
result = publisher.sync_product("uuid-do-produto")

if result.success:
    print(f"Produto sincronizado: {result.data}")
else:
    print(f"Erro: {result.error}")
""")

    print("=" * 60)
