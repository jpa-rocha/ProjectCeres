import { createParamDecorator, ExecutionContext } from "@nestjs/common";

// Custom decorator declaration, switches execution context to http,
// and gets request with appropriate data.
// Keeps nestjs level of abstraction without forcing the use of express.
export const GetUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx
      .switchToHttp()
      .getRequest();
    if (data) {
      return request.user[data];
    }
    return request.user;
  },
);
