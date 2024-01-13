from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from registration_form_with_db.model import User


# добавлена проверка наличия/отсутствия пользователя с одинаковым email в нашей базе данных
class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    first_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Отправка данных')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Пользователь с таким email уже существует')
