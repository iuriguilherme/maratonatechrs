"""Forms"""

import logging
from quart_wtf import QuartForm
from wtforms import (
  DecimalField,
  EmailField,
  # ~ Form,
  HiddenField,
  # ~ IntegerField,
  PasswordField,
  RadioField,
  # ~ SelectField,
  StringField,
  SubmitField,
  TextAreaField,
  # ~ validators,
)
from wtforms.validators import (
  DataRequired,
  Email,
  EqualTo,
)
from wtforms.widgets import PasswordInput

logger: logging.Logger = logging.getLogger(__name__)

class RenderDecimalField(DecimalField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class RenderEmailField(EmailField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class RenderPasswordField(PasswordField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class RenderRadioField(RadioField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class RenderStringField(StringField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class RenderTextAreaField(TextAreaField):
  def __init__(self, *args, **kwargs) -> None:
    self.render: bool = kwargs.pop('render', False)
    super().__init__(*args, **kwargs)

class MarkerForm(QuartForm):
  """Formulário para adicionar marcador"""
  latitude_field: RenderDecimalField = RenderDecimalField(
    "Latitude",
    validators = [DataRequired()],
    default = -30.028344,
    render = True,
  )
  longitude_field: RenderDecimalField = RenderDecimalField(
    "Longitude",
    validators = [DataRequired()],
    default = -51.228529,
    render = True,
  )
  description_field: RenderStringField = RenderStringField(
    "Descrição",
    validators = [
      DataRequired(),
    ],
    default = "Porto Alegre",
    render = True,
  )
  submit_field: SubmitField = SubmitField("Cadastrar")

class UserLoginForm(QuartForm):
  """Formulário de login de usuário"""
  username_field: RenderStringField = RenderStringField(
    "Nome de usuário",
    validators = [
      DataRequired(),
    ],
    render = True,
  )
  password_field: RenderPasswordField = RenderPasswordField(
    "Senha",
    widget = PasswordInput(hide_value = False),
    validators = [
      DataRequired(),
    ],
    render = True,
  )
  submit_field: SubmitField = SubmitField("Login")

class UserRegisterForm(QuartForm):
  """Formulário para registro de usuário"""
  username_field: RenderStringField = RenderStringField(
    "Nome de usuário",
    validators = [
      DataRequired(),
    ],
    render = True,
  )
  password_field: RenderPasswordField = RenderPasswordField(
    "Senha",
    widget = PasswordInput(hide_value = False),
    validators = [
      DataRequired(),
      EqualTo(
        "confirm_field",
        message = "As senhas não são iguais",
      ),
    ],
    render = True,
  )
  confirm_field: RenderPasswordField = RenderPasswordField(
    "Senha novamente",
    widget = PasswordInput(hide_value = False),
    validators = [
      DataRequired(),
    ],
    render = True,
  )
  level_field: RenderRadioField = RenderRadioField(
    "Nível de permissão",
    validators = [DataRequired()],
    choices = [
      ("0", "Depuração (pode fazer tudo - não usar)"),
      ("1", "Desenvolvedor (acesso a todas rotas)"),
      ("2", "Administrador (acesso a funções de administração do sistema"),
      ("3", "Usuário (tem acesso às páginas de usuário)"),
      ("4", "Visitante (não pode fazer nada)"),
    ],
    render = True,
  )
  active_field: RenderRadioField = RenderRadioField(
    "Conta ativa?",
    validators = [DataRequired()],
    choices = [("0", "Inativa"), ("1", "Ativa")],
    render = True,
  )
  submit_field: SubmitField = SubmitField("Atualizar")

class UserSettingsForm(QuartForm):
  """Formulário para preferências de usuário"""
  user_id_field: HiddenField = HiddenField("user_id", default = "0")
  nome_field: RenderStringField = RenderStringField(
    "Nome",
    validators = [DataRequired()],
    render = True,
  )
  submit_field: SubmitField = SubmitField("Atualizar")
