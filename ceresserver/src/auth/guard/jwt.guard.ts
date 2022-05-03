import { AuthGuard } from "@nestjs/passport";

// Prevents the use of strings in guards in several different location.
export class JwtGuard extends AuthGuard('jwt') {
  constructor () {
    super();
  }
}
