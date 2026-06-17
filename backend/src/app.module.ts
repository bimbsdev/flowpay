import { Module } from '@nestjs/common'
import { ConfigModule } from '@nestjs/config'
import { APP_INTERCEPTOR } from '@nestjs/core'
import { AppController } from './app.controller'
import { AppService } from './app.service'
import { AuthModule } from './auth/auth.module'
import { DripsModule } from './drips/drips.module'
import { PaymentsModule } from './payments/payments.module'
import { WorkflowsModule } from './workflows/workflows.module'
import { RateLimitInterceptor } from './common/interceptors/rate-limit.interceptor'

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      // Validate required environment variables on startup
      validate: (config) => {
        const requiredVars = [
          'NODE_ENV',
          'API_PORT',
          'STELLAR_NETWORK',
          'STELLAR_RPC_URL',
        ]
        const missing = requiredVars.filter((v) => !config[v])
        if (missing.length > 0) {
          throw new Error(`Missing required env vars: ${missing.join(', ')}`)
        }
        return config
      },
    }),
    AuthModule,
    WorkflowsModule,
    DripsModule,
    PaymentsModule,
  ],
  controllers: [AppController],
  providers: [
    AppService,
    {
      provide: APP_INTERCEPTOR,
      useClass: RateLimitInterceptor,
    },
  ],
})
export class AppModule {}
