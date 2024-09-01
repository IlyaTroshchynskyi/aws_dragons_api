resource "aws_cognito_user_pool" "dragons-user-pool" {
  name                     = "${var.user_pool_name}-${var.environment}"
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  password_policy {
    minimum_length    = 6
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name            = "${var.user_pool_name}-client-${var.environment}"
  user_pool_id    = aws_cognito_user_pool.dragons-user-pool.id
  generate_secret = false

  supported_identity_providers = ["COGNITO"]
  callback_urls                = ["https://example.com/callback"]
  logout_urls                  = ["https://example.com/signout"]
  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

  token_validity_units {
    access_token  = "minutes"
    refresh_token = "minutes"
  }

  access_token_validity  = 5
  refresh_token_validity = 60

}