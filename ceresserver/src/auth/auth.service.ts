import { ForbiddenException, Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AuthDto } from './dto';
import * as argon from 'argon2';
import { PrismaClientKnownRequestError } from '@prisma/client/runtime';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';


@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwt: JwtService,
    private config: ConfigService) {}
  
  // signup function takes the authentication dto and creates a user in the db
  // using prisma. In case of error, they should be descriminated.
  // CURRENTLY ONLY DUPLICATE USER IS TAKEN
  async signup(dto: AuthDto) {
    try {
      const hash = await argon.hash(dto.password);
      const user = await this.prisma.user.create({
        data: {
          email: dto.email,
          hash: hash,
          userName: dto.userName,
          firstName: dto.firstName,
          lastName: dto.lastName,
        }
      })
      
      return this.signToken(user.id, user.userName, user.admin, user.email);
    } catch(error) {
        if (error instanceof PrismaClientKnownRequestError) {
          if (error.code === 'P2002') {
            throw new ForbiddenException(
              'Credentials taken',
            );
          }
      }
	throw error;
      }
  }
  
  // signin takes in the authentication dto and searches the db with prisma
  // for the username (unique field), if no user name is found an error is thrown.
  // If a valid username is found the password is matched to the hash stored in the db,
  // in case this password is invalid an error is thrown.
  // The function returns a signed JWT that allows the user to further navigate.
  async signin(dto: AuthDto) {
    const user = await this.prisma.user.findUnique({
      where: {
	userName: dto.userName,
      },
    });
    if (!user) throw new ForbiddenException(
      'User does not exist.',
    );
    const pwMatches = await argon.verify(
      user.hash,
      dto.password,
    );
    if (!pwMatches)
      throw new ForbiddenException(
	'Invalid password',
    );
   
    return this.signToken(user.id, user.userName, user.admin, user.email);
  }

  // signToken tokenizes the user information so it is passed in a
  // safe format to the browser, session duration is controled here.
  async signToken(
    userId: number,
    userName: string,
    admin: number,
    email: string
  ): Promise<{ access_token: string }> {
    const payload = {
      sub:userId,
	  userName,
	  admin,
	  email
    };
    const secret = this.config.get('JWT_SECRET');
    const token = await this.jwt.signAsync(
      payload,
      {
	expiresIn: '60m',
	secret: secret
      },
    );
    
    return {
      access_token: token,
    };
  }
}
