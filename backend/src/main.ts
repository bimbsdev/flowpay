import { ValidationPipe } from '@nestjs/common'
import { NestFactory } from '@nestjs/core'
import { AppModule } from './app.module'
import { AllExceptionsFilter } from './common/filters/http-exception.filter'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)

  // Global exception filter
  app.useGlobalFilters(new AllExceptionsFilter())

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  )

  // Enable CORS
  app.enableCors()

  const port = process.env.API_PORT || 3001
  await app.listen(port, () => {
    console.log(`🚀 FlowPay API running on port ${port}`)
  })
}

bootstrap()
